from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import find_in_bag, check_location
from models import hero
from models.hero_context import hero_context


async def go_deposit_items(context:hero_context ,action:ActionController,db:DbController, resource_code=None ):
  print(f'{context.current_hero.name} will now deposit items to the bank!')
  qtty = None
  if resource_code:
    qtty = find_in_bag(context.current_hero.inventory, resource_code)

  dest = await db.get_closest_map(context, content_type="bank", content_code="bank")
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    print(f'Moving to the bank : {dest.x} {dest.y}')
    context = await action.hero.move(context, dest.x, dest.y)
    
  context = await action.bank.deposit(context, resource_code, qtty)

  return context