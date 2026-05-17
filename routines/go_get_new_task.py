from controllers import ActionController, DbController
from helpers import check_location
from models import hero


async def go_get_new_task(context, action:ActionController, db:DbController, task_type:str):
  dest = await db.get_closest_map(context, content_type="tasks_master", content_code=task_type)
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    print(f'Moving to the task master : {dest.x} {dest.y}')
    my_hero = await action.move(context, dest.x, dest.y)
    
  my_hero = await action.accept_new_task(context)

  return my_hero