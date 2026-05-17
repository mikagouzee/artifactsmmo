from dataclasses import replace
from controllers import ActionController, DbController
from helpers import check_bag_weight, check_location
from .go_equip import go_equip

async def go_gather(context,action:ActionController,db:DbController, resource_code, tool_code:str=None):
  
  print(f'{context.current_hero.name} will now gather {resource_code}')
  if tool_code and context.current_hero.weapon_slot != tool_code:
    # print(f'{context.current_hero.name} wants to equip {tool_code}')
    context = await go_equip(context, tool_code, action, db, slot="weapon", quantity=1)

  dest = await db.get_closest_map(context.current_hero, content_type="resource", content_code=resource_code)

  if dest and not check_location(context.current_hero, dest.x, dest.y):
    context = await action.hero.move(context, dest.x, dest.y)

  max_weight = context.current_hero.inventory_max_items

  while (check_bag_weight(context.current_hero.inventory) < max_weight ):
    context = await action.hero.gather(context)

  return context