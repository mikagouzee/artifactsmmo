# db_controller.py
from managers.db_manager import DatabaseManager
from models.map_tile import MapTile

class DbController:
    def __init__(self, http_client):
        self.http = http_client

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

    async def get_closest_map(self, hero, content_code: str, content_type:str):
        collection = DatabaseManager.db["map_tiles"]
        
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