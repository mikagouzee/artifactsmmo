
from controllers import ActionController, db_controller
from helpers import find_in_bag, check_location
from models import hero


async def go_equip(context, item_code, action:ActionController,db:db_controller, slot="weapon", quantity=1):
  print(f'{context.current_hero.name} will try to equip {item_code}.')
  if context.current_hero.weapon_slot == item_code:
    return context

  if find_in_bag(context.current_hero.inventory, item_code):
    print(f'{context.current_hero.name} found {item_code} in their bag!.')
    context = await action.hero.equip(context.current_hero, item_code, slot=slot, qtty=quantity)
  else:
    dest = await db.get_closest_map(context.current_hero, content_code='bank', content_type='bank')
    if dest and not check_location(context.current_hero, dest.x, dest.y):
      print(f'{context.current_hero.name} did NOT found {item_code} in their bag : moving to the bank {dest.x} {dest.y}.')
      context = await action.hero.move(context, dest.x, dest.y)
      print(f'Trying to withdraw {item_code} for {context.current_hero.name}')
      context = await action.bank.withdraw(context, item_code, 1)

      if find_in_bag(context.current_hero.inventory, item_code):
        print({f'There was a {item_code} in the bank -> equipping.'})
        context = await action.hero.equip(context.current_hero, item_code, slot=slot, qtty=quantity)
      else:
        print(f"You don't have any {item_code} ! Try crafting one")

  return context