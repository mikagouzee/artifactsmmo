from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import check_location, check_quantity_in_bag, find_max_craftable_quantity
from models import item
from routines import go_craft, go_withdraw_items

async def go_produce(context, action:ActionController,db:DbController, desired:item):  
   
  items_in_bank = await action.bank.get_bank_inventory()
  in_pockets = [{ "code":item["code"] , "quantity":item["quantity"] } for item in context.current_hero.inventory]
  total_craft_possible = find_max_craftable_quantity(items_in_bank+in_pockets, desired)
  
  available_space = context.current_hero.inventory_max_items - sum((x["quantity"] for x in context.current_hero.inventory))
  ingredient_list = desired["craft"]["items"]
  items_per_craft = sum(a["quantity"] for a in ingredient_list)

  max_crafts_by_weight = available_space // items_per_craft

  can_carry = min(total_craft_possible, max_crafts_by_weight)

  needed_items = []

  for ingredient in ingredient_list:
    total_needed = ingredient["quantity"] * can_carry
  
    in_pockets = check_quantity_in_bag(context.current_hero.inventory, ingredient["code"])
    can_carry += (in_pockets/ingredient["quantity"])
    amount_to_withdraw = max(0, total_needed - in_pockets)
    
    if amount_to_withdraw > 0:
      needed_items.append({
        "code":ingredient["code"],
        "quantity":amount_to_withdraw
      })
      context = await go_withdraw_items(context, action, db, needed_items)

  context = await go_craft(context, action, db, desired, can_carry)

  return context

