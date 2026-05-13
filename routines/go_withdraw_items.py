from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import check_bag_weight, find_in_bag, check_location
from models import hero
from routines import go_deposit_item


async def go_withdraw_items(my_hero,action:ActionController,db:DbController, items_list: list):
  print(f'{my_hero.name} will now withdraw items to the bank!')
  
  max_weight = my_hero.inventory_max_items
  current_weight = check_bag_weight(my_hero.inventory)
  expected_weight_to_withdraw = check_bag_weight(items_list)

  if (current_weight + expected_weight_to_withdraw > max_weight):
    my_hero = await go_deposit_item(my_hero, action, db)
  # if current_weight == max_weight

  dest = await db.get_closest_map(my_hero, content_type="bank", content_code="bank")
  
  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f'Moving to the bank : {dest.x} {dest.y}')
    my_hero = await action.move(my_hero, dest.x, dest.y)
  
  
  my_hero = await action.withdraw_items(my_hero, items_list)

  return my_hero