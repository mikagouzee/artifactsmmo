from dataclasses import replace
from controllers import get_closest_map, move, craft
from controllers.action_controller import ActionController
from helpers import check_skill_level, check_location, check_ingredient_list
from models import item

async def go_craft(my_hero, controller:ActionController, desired:item, workshop_code:str, qtty:int=1):  
  print(f"{my_hero.name} will now try to craft {desired.code} at {workshop_code}")
  if not can_craft(my_hero, desired.craft):
    return my_hero

  dest = await controller.get_closest_map(my_hero, content_type="workshop", content_code=workshop_code)
  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f"{my_hero.name} moves to {dest.x} {dest.y}")
    my_hero = await controller.move(my_hero, dest.x, dest.y)
  
  while(can_craft(my_hero, desired.craft)):
    my_hero = await controller.craft(my_hero, desired.code, qtty)

  return my_hero

def can_craft(my_hero, craft):
  return check_skill_level(my_hero, craft) and check_ingredient_list(my_hero.inventory, craft)



    
  