# db_controller.py
from controllers.managers import resource_manager
from managers import monster_manager
from controllers.managers.db_manager import DatabaseManager
from controllers.managers.item_manager import item_manager
from models.map_tile import MapTile

class DbController:
    def __init__(self, http_client):
        self.http = http_client
        self.item = item_manager()
        self.monster = monster_manager()
        self.resource = resource_manager()

    async def sync_resources(self):
        collection = DatabaseManager.db["resources"]
        
        response = await self.http.get("/resources")
        resources = response.json().get("data", [])

        for res in resources:
            await collection.replace_one(
                {"code": res["code"]},
                res,
                upsert=True
            )
        print(f"Synced {len(resources)} resources.")

    async def sync_world_map(self):
        collection = DatabaseManager.db["map_tiles"]
        page = 1
        
        while True:
            response = await self.http.get("/maps", params={"page": page, "size": 100})
            data = response.json()
            maps_data = data.get("data", [])

            for tile in maps_data:
                await collection.replace_one(
                    {"x": tile["x"], "y": tile["y"], "layer":tile["layer"]}, # Clé unique par coordonnées
                    tile,
                    upsert=True
                )

            if page >= data.get("pages", 1):
                break
            page += 1
        print("Synced WorldMap.")

    async def sync_items(self):
        collection = DatabaseManager.db["items"]
        page = 1
        
        while True:
            response = await self.http.get("/items", params={"page": page, "size": 100})
            data = response.json()
            items_data = data.get("data", [])

            for item in items_data:
                await collection.replace_one(
                    {"name": item["name"], "code":item["code"]},
                    item,
                    upsert=True
                )

            if page >= data.get("pages", 1):
                break
            page += 1
        print(f"Synced {len(items_data)} Items.")

    async def sync_monsters(self):
        collection = DatabaseManager.db["monsters"]
        page = 1
        
        while True:
            response = await self.http.get("/monsters?min_level=1", params={"page": page, "size": 100})
            data = response.json()
            monsters_data = data.get("data", [])

            for monster in monsters_data:
                await collection.replace_one(
                    {"name": monster["name"], "code":monster["code"]},
                    monster,
                    upsert=True
                )

            if page >= data.get("pages", 1):
                break
            page += 1
        print(f"Synced {len(monsters_data)} Monsters.")

    async def sync_data(self):
        map_count = await DatabaseManager.db["map_tiles"].count_documents({})
        if map_count == 0:
            await self.sync_world_map()

        res_count = await DatabaseManager.db["resources"].count_documents({})
        if res_count == 0:
            await self.sync_resources()

        monster_count = await DatabaseManager.db["monsters"].count_documents({})
        if monster_count == 0:
            await self.sync_monsters()

        items_count = await DatabaseManager.db["items"].count_documents({})
        if items_count == 0:
            await self.sync_items()

    async def get_closest_map(self, context, content_code: str, content_type:str):
        collection = DatabaseManager.db["map_tiles"]
        hero = context.current_hero
        cursor = collection.find({"interactions.content.code": content_code, "interactions.content.type":content_type})
        targets = await cursor.to_list(length=100)
        
        if not targets:
            return None
        
        # Calcul de la distance de Manhattan : |x1-x2| + |y1-y2|
        closest = min(
            targets, 
            key=lambda t: abs(t["x"] - hero.x) + abs(t["y"] - hero.y)
        )
        if closest:
            tile_obj = MapTile.model_validate(closest)
            return tile_obj
        
    async def find_best_craft(self, my_hero, skill_name, bank_inventory=None):
    # Get the hero's current skill level
        skill_level_attr = f"{skill_name}_level"
        if not hasattr(my_hero, skill_level_attr):
            return None
        
        current_skill_level = getattr(my_hero, skill_level_attr)
        min_level_to_progress = current_skill_level - 10

        # Query items collection for craftable items
        collection = DatabaseManager.get_collection("items")
        
        # Find items with craft recipes for this skill, at or below current skill level
        query = {
            "craft.skill": skill_name,
            "craft.level": {"$lte": current_skill_level, "$gt": min_level_to_progress}
        }
        
        candidates = await collection.find(query).to_list(length=None)
        
        if not candidates:
            return None
        
        # Create a combined inventory lookup from both bank and hero inventory
        combined_inventory = get_available_resources(bank_inventory, my_hero.inventory)
        
        best_item = None
        best_craftable_qty = 0
        best_ingredient_count = float('inf')
        best_level = -1
        
        for item in candidates:
            # Get recipe details
            recipe = item.get("craft", {})
            required_items = recipe.get("items", [])
            required_quantity = recipe.get("quantity", 1)
            item_level = item.get("level", 0)
            
            # Calculate how many times we can craft this item
            craftable_qty = float('inf')
            
            for required in required_items:
                ingredient_code = required.get("code")
                ingredient_qty = required.get("quantity", 0)
                
                available_qty = combined_inventory.get(ingredient_code, 0)
                
                # How many crafts can we do with this ingredient?
                times_can_craft = available_qty // ingredient_qty if ingredient_qty > 0 else 0
                
                # The bottleneck ingredient determines how many we can craft
                craftable_qty = min(craftable_qty, times_can_craft)
            
            # If we can't craft it, skip
            if craftable_qty <= 0 or craftable_qty == float('inf'):
                continue
            
            # Total quantity of items we'd get
            final_qty = craftable_qty * required_quantity
            
            # Determine if this is better than our current best
            # Priority: higher level > fewer ingredients > more craftable quantity
            is_better = False
            
            if item_level > best_level:
                is_better = True
            elif item_level == best_level:
                if len(required_items) < best_ingredient_count:
                    is_better = True
                elif len(required_items) == best_ingredient_count and final_qty > best_craftable_qty:
                    is_better = True
            
            if is_better:
                best_item = item
                best_craftable_qty = final_qty
                best_ingredient_count = len(required_items)
                best_level = item_level
        
        if best_item is None:
            return None
        
        return (best_item, best_craftable_qty)