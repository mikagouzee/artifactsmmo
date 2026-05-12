from controllers import ActionController, DbController
from helpers import check_location
from models import hero


async def go_deposit_gold(my_hero,action:ActionController,db:DbController):
  print(f'{my_hero.name} will now deposit {my_hero.gold} gold to the bank!')

  dest = await db.get_closest_map(my_hero, content_type="bank", content_code="bank")
  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f'Moving to the bank : {dest.x} {dest.y}')
    my_hero = await action.move(my_hero, dest.x, dest.y)
    
  my_hero = await action.deposit_gold(my_hero)

  return my_hero