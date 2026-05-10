from dataclasses import replace
from controllers import get_closest_map, use_item, move, rest, fight
from controllers.action_controller import ActionController
from helpers import find_in_bag, check_location, check_bag_weight
from models import hero


async def go_fight(my_hero, monster_code, controller:ActionController):
  print(f'{my_hero.name} will try to fight {monster_code}.')
  dest = await controller.get_closest_map(my_hero, content_type="monster", content_code=monster_code)
  
  # if not find_in_bag(my_hero.inventory, "small_health_potion"):
  #   my_hero = await controller.withdraw(my_hero, "small_health_poition", 20)
  #   my_hero = await controller.equip(my_hero, "small_health_potion", 1)

  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f'{my_hero.name} moving to {dest.x}{dest.y} to fight!')
    my_hero = await controller.move(my_hero, dest.x, dest.y)

  max_weight = my_hero.inventory_max_items

  while check_bag_weight(my_hero.inventory) < max_weight:
    if my_hero.hp < my_hero.max_hp:
      if find_in_bag(my_hero.inventory, 'cooked_chicken') > 0:
        print(f'{my_hero.name} eating to restore life.')
        my_hero = await controller.use_item(my_hero, 'cooked_chicken')
      elif my_hero.hp <= my_hero.max_hp /2:
        print(f'{my_hero.name} resting to restore life : it\'s Nap Time.')
        my_hero = await controller.rest(my_hero)
      else:        
        if dest and not check_location(my_hero, dest.x, dest.y):
          print(f'{my_hero.name} moving to {dest.x}{dest.y} to fight!')
          my_hero = await controller.move(my_hero, dest.x, dest.y)
          
        my_hero = await controller.fight(my_hero)
    else:
      if dest and not check_location(my_hero, dest.x, dest.y):
        print(f'{my_hero.name} moving to {dest.x}{dest.y} to fight!')
        my_hero = await controller.move(my_hero, dest.x, dest.y)
      my_hero = await controller.fight(my_hero)

  return my_hero