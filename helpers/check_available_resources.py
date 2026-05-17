def check_available_resources(bank_inventory, hero_inventory):
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