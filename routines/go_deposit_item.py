from dataclasses import replace
from controllers import get_closest_map, move
from controllers.action_controller import ActionController
from controllers.deposit import deposit
from helpers import find_in_bag, check_location
from models import hero


async def go_deposit_item(my_hero,controller:ActionController, resource_code=None ):
  print(f'{my_hero.name} will now deposit items to the bank!')
  qtty = None
  if resource_code:
    qtty = find_in_bag(my_hero.inventory, resource_code)

  dest = await controller.get_closest_map(my_hero, content_type="bank", content_code="bank")
  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f'Moving to the bank : {dest.x} {dest.y}')
    my_hero = await controller.move(my_hero, dest.x, dest.y)
    
    my_hero = await controller.deposit(my_hero, resource_code, qtty)

  return my_hero