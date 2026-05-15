def find_max_craftable_quantity(bag, item):
    bag = {item["code"]:item["quantity"] for item in bag}

    recipe = item.get("craft", {})
    required_items = recipe.get("items", [])
    craft_quantity = recipe.get("quantity", 1)
    
    craftable_qty = float('inf')
    
    for ingredient in required_items:
        ingredient_code = ingredient.get("code")
        ingredient_qty = ingredient.get("quantity", 0)
        
        available_qty = bag.get(ingredient_code, 0)
        
        # How many crafts can we do with this ingredient?
        times_can_craft = available_qty // ingredient_qty if ingredient_qty > 0 else 0
        
        # The bottleneck ingredient determines how many we can craft
        craftable_qty = min(craftable_qty, times_can_craft)
    
    # If we can't craft it, skip
    if craftable_qty <= 0 or craftable_qty == float('inf'):
        return 0
    
    # Total quantity of items we'd get
    return craftable_qty * craft_quantity