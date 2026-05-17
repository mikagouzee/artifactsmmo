from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import check_skill_level, check_location, check_ingredient_list
from models import item

async def go_craft(context, action:ActionController,db:DbController, desired:item, qtty:int=1):  
  
  print(f"{context.current_hero.name} will now try to craft {desired["code"]} at {desired["craft"]["skill"]}")
  if not can_craft(context.current_hero, desired["craft"]):
    return context.current_hero

  context = await go_to_workshop(context.current_hero, desired["craft"]["skill"], db, action)  
  
  context = await action.hero.craft(context.current_hero, desired["code"], qtty)

  return context

def can_craft(context, craft):
  return check_skill_level(context.current_hero, craft) and check_ingredient_list(context.current_hero.inventory, craft)

async def go_to_workshop(context, workshop_code, db, action):
  dest = await db.get_closest_map(context, content_type="workshop", content_code=workshop_code)
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    print(f"{context.current_hero.name} moves to {dest.x} {dest.y}")
    return await action.hero.move(context, dest.x, dest.y)
  