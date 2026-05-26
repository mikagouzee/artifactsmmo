
# from models.bag import Bag


def check_can_craft(context, craft):
  # bag = Bag(context.current_hero.inventory)
  return check_craft_level(context.current_hero, craft) and check_ingredient_list(context.current_hero.inventory, craft)
  #and bag.has_ingredients(craft)

def check_craft_level(my_hero, craft):
  skillname = craft["skill"]
  skillname+="_level"
  skill = getattr(my_hero, skillname)
  if skill >= craft["level"]:
    return True
  
  return False

def find_max_craftable_quantity(bag, item):
    if isinstance(bag, list):
      bag = {thing["code"]:thing["quantity"] for thing in bag}

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

def check_ingredient_list(bag, craft):
  for ingredient in craft["items"]:
    hold_qty = check_quantity_in_bag(bag, ingredient["code"])
    if  hold_qty < ingredient["quantity"]:
      print(f"Missing {ingredient["quantity"] - hold_qty} {ingredient["code"]} ! Can't proceed with craft")
      return False
  return True  

def check_quantity_in_bag(bag, item_code):
  if isinstance(bag, dict):
    bag = [{"code":k, "quantity": v} for k, v in bag.items()]
  return next((x["quantity"] for x in bag if x["code"] == item_code), 0)