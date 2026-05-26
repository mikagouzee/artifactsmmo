from dataclasses import replace
from controllers import ActionController
from controllers.db_controller import DbController
from helpers import check_bag_weight, check_quantity_in_bag, check_location
from models.hero_context import hero_context
from townhall import town_hall


async def go_deposit_items(context:hero_context ,action:ActionController,db:DbController, resource_code=None ):
  if check_bag_weight(context.current_hero.inventory) == 0:
     return context

  qtty = None
  if resource_code:
    qtty = check_quantity_in_bag(context.current_hero.inventory, resource_code)

  dest = await db.get_closest_map(context, content_type="bank", content_code="bank")
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    print(f'Moving to the bank : {dest.x} {dest.y}')
    context = await action.hero.move(context, dest.x, dest.y)
    
  context = await action.bank.deposit(context, resource_code, qtty)
  await town_hall.refresh_bank_cache()
  return context