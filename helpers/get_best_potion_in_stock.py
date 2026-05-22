
def get_best_potion_in_stock(context, bank_bag, healing_potions):
  available = []

  for item in bank_bag:
    if item.get("subtype") == "potion":
      available.append({
        "item_code":item["code"],
        "value":item["effects"]["value"]
      })

  for item in context.current_hero.inventory:
    if item["code"] in healing_potions:
      available.append({
        "item_code":item["code"],
        "value":healing_potions[item["code"]]["effects"]["value"]
      })

  if not available:
    return None
  
  target_hp = context.current_hero.max_hp
  target_potion = min(available, key=lambda x: abs(x["value"] - target_hp))
  
  return target_potion