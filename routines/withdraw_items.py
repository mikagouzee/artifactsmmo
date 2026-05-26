from controllers import ActionController
from controllers.db_controller import DbController
from helpers import check_bag_weight, check_location
from townhall import town_hall


async def go_withdraw_items(context,action:ActionController,db:DbController, items_list: list):
  dest = await db.get_closest_map(context, content_type="bank", content_code="bank")  
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    context = await action.hero.move(context, dest.x, dest.y)  

  max_weight = context.current_hero.inventory_max_items
  current_weight = check_bag_weight(context.current_hero.inventory)
  expected_weight_to_withdraw = check_bag_weight(items_list)

  if (current_weight + expected_weight_to_withdraw > max_weight):
    context = await action.bank.deposit_all_but(context, items_list)
  
  context = await action.bank.withdraw_items(context, items_list)
  await town_hall.refresh_bank_cache()

  return context