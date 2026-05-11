
from controllers.action_controller import ActionController
from helpers import find_in_bag, check_location
from models import hero


async def go_equip(my_hero, item_code, controller:ActionController, slot="weapon", quantity=1):
  print(f'{my_hero.name} will try to equip {item_code}.')
  if my_hero.weapon_slot == item_code:
    return my_hero

  if find_in_bag(my_hero.inventory, item_code):
    print(f'{my_hero.name} found {item_code} in their bag!.')
    my_hero = await controller.equip(my_hero, item_code, slot=slot, qtty=quantity)
  else:
    dest = await controller.get_closest_map(my_hero, content_code='bank', content_type='bank')
    if dest and not check_location(my_hero, dest.x, dest.y):
      print(f'{my_hero.name} dit NOT found {item_code} in their bag : moving to the bank {dest.x} {dest.y}.')
      my_hero = await controller.move(my_hero, dest.x, dest.y)
      print(f'Trying to withdraw {item_code} for {my_hero.name}')
      my_hero = await controller.withdraw(my_hero, item_code, 1)
      
      if find_in_bag(my_hero.inventory, item_code):
        print({f'There was a {item_code} in the bank -> equipping.'})
        my_hero = await controller.equip(my_hero, item_code, slot=slot, qtty=quantity)
      else:
        print(f"You don't have any {item_code} ! Try crafting one")

  return my_hero