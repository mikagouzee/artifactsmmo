from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import check_skill_level, check_location, check_ingredient_list
from models import item

async def go_craft(my_hero, action:ActionController,db:DbController, desired:item, qtty:int=1):  
  print(f"{my_hero.name} will now try to craft {desired["code"]} at {desired["craft"]["skill"]}")
  if not can_craft(my_hero, desired["craft"]):
    return my_hero

  my_hero = await go_to_workshop(my_hero, desired["craft"]["skill"], db, action)  
  
  my_hero = await action.craft(my_hero, desired["code"], qtty)

  return my_hero

def can_craft(my_hero, craft):
  return check_skill_level(my_hero, craft) and check_ingredient_list(my_hero.inventory, craft)

async def go_to_workshop(my_hero, workshop_code, db, action):
  dest = await db.get_closest_map(my_hero, content_type="workshop", content_code=workshop_code)
  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f"{my_hero.name} moves to {dest.x} {dest.y}")
    return await action.move(my_hero, dest.x, dest.y)
  