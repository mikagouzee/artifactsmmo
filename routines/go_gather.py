from dataclasses import replace
from controllers import ActionController, DbController
from helpers import check_bag_weight, check_location
from .go_equip import go_equip

async def go_gather(my_hero,action:ActionController,db:DbController, resource_code, tool_code:str=None):
  print(f'{my_hero.name} will now gather {resource_code}')
  if tool_code and my_hero.weapon_slot != tool_code:
    # print(f'{my_hero.name} wants to equip {tool_code}')
    my_hero = await go_equip(my_hero, tool_code, action)

  dest = await db.get_closest_map(my_hero, content_type="resource", content_code=resource_code)

  if dest and not check_location(my_hero, dest.x, dest.y):
    # print(f'{my_hero.name} moves to {dest.x} {dest.y}')
    my_hero = await action.move(my_hero, dest.x, dest.y)

  max_weight = my_hero.inventory_max_items

  while (check_bag_weight(my_hero.inventory) < max_weight ):
    # print(f'{my_hero.name} is gathering.')
    my_hero = await action.gather(my_hero)
    
  return my_hero