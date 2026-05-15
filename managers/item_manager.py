from managers.db_manager import DatabaseManager
from models import hero


async def find_best_craft_item(my_hero: hero, skill_name: str, bank_inventory: list = None) -> tuple | None:
 
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




def get_available_resources(bank_inventory, hero_inventory):
    if bank_inventory is None:
        bank_inventory = []

    combined_inventory = {item["code"]: item["quantity"] for item in bank_inventory}
    
    # Add hero inventory items
    if hero_inventory:
        for inv_item in hero_inventory:
            code = inv_item["code"]
            qty = inv_item["quantity"]
            # Combine quantities if item exists in both
            combined_inventory[code] = combined_inventory.get(code, 0) + qty

    return combined_inventory

async def find_item_by_code(item_code):
    collection = DatabaseManager.get_collection("items")
    query = {
        "code":item_code
    }
    queried = await collection.find(query).to_list(length=1)
    return queried[0]

