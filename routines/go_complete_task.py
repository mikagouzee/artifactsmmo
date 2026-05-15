from controllers import ActionController, DbController
from helpers import check_location
from models import hero


async def go_complete_task(my_hero, action:ActionController, db:DbController):
  dest = await db.get_closest_map(my_hero, content_type="tasks_master", content_code=my_hero.task_type)
  if dest and not check_location(my_hero, dest.x, dest.y):
    print(f'Moving to the task master : {dest.x} {dest.y}')
    my_hero = await action.move(my_hero, dest.x, dest.y)
    
  # if my_hero.task_type == "items":
  #   my_hero = await action.task_trade(my_hero)
  
  my_hero = await action.complete_task(my_hero)

  return my_hero