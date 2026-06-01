from controllers import ActionController, DbController
from helpers import check_location, check_quantity_in_bag
from models import hero


async def go_trade_task(context, action:ActionController, db:DbController):
  my_hero = context.current_hero
  if not check_quantity_in_bag(my_hero.inventory, my_hero.task):
    return context    
  
  dest = await db.get_closest_map(context, content_type="tasks_master", content_code=my_hero.task_type)
  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f"[{my_hero.name}] Moving to the task master: {dest.x} {dest.y}")
    context = await action.hero.move(context, dest.x, dest.y)

  still_missing = my_hero.task_total - my_hero.task_progress
  quantity = min(still_missing, check_quantity_in_bag(my_hero.inventory, my_hero.task))
  context = await action.task.task_trade(context, quantity)

  return context