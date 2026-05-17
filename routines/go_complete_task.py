from controllers import ActionController, DbController
from helpers import check_location
from models import hero


async def go_complete_task(context, action:ActionController, db:DbController):
  dest = await db.get_closest_map(context, content_type="tasks_master", content_code=context.task_type)
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    context = await action.move(context, dest.x, dest.y)
      
  context = await action.complete_task(context)

  return context