from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import check_bag_weight, find_in_bag, check_location
from models import hero
from routines import go_deposit_items


async def go_withdraw_items(context,action:ActionController,db:DbController, items_list: list):
  print(f'{context.current_hero.name} will now withdraw items from the bank!')
  
  max_weight = context.current_hero.inventory_max_items
  current_weight = check_bag_weight(context.current_hero.inventory)
  expected_weight_to_withdraw = check_bag_weight(items_list)

  if (current_weight + expected_weight_to_withdraw > max_weight):
    context = await go_deposit_items(context, action, db)
  
  dest = await db.get_closest_map(context, content_type="bank", content_code="bank")
  
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    # print(f'Moving to the bank : {dest.x} {dest.y}')
    context = await action.hero.move(context, dest.x, dest.y)
  
  context = await action.bank.withdraw_items(context, items_list)

  return context