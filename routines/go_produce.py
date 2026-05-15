from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import find_in_bag, find_max_craftable_quantity
from models import item
from routines import go_craft, go_withdraw_items

async def go_produce(my_hero, action:ActionController,db:DbController, desired:item):  
   
  items_in_bank = await action.get_bank_inventory()

  bank_bag = {item["code"]:item["quantity"] for item in items_in_bank}

  if my_hero.inventory:
    for inv_item in my_hero.inventory:
      code = inv_item["code"]
      qty = inv_item["quantity"]
      # Combine quantities if item exists in both
      bank_bag[code] = bank_bag.get(code, 0) + qty

  total_craft_possible = find_max_craftable_quantity(bank_bag, desired)
  
  available_space = my_hero.inventory_max_items - sum((x["quantity"] for x in my_hero.inventory))
  ingredient_list = desired["craft"]["items"]
  items_per_craft = sum(a["quantity"] for a in ingredient_list)

  max_crafts_by_weight = available_space // items_per_craft

  can_carry = min(total_craft_possible, max_crafts_by_weight)

  needed_items = []

  for ingredient in ingredient_list:
    total_needed = ingredient["quantity"] * can_carry
  
    in_pockets = find_in_bag(my_hero.inventory, ingredient["code"])
    amount_to_withdraw = max(0, total_needed - in_pockets)

    if amount_to_withdraw > 0:
      needed_items.append({
        "code":ingredient["code"],
        "quantity":amount_to_withdraw
      })

  my_hero = await go_withdraw_items(my_hero, action, db, needed_items)

  my_hero = await go_craft(my_hero, action, db, desired, can_carry)

  return my_hero