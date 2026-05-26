from controllers import ActionController, DbController
from helpers import check_can_craft, check_location
from models import item

async def go_craft(context, action:ActionController,db:DbController, desired:item, qtty:int=1):  
  
  print(f"{context.current_hero.name} will now try to craft {desired["code"]} at {desired["craft"]["skill"]}")
  if not check_can_craft(context, desired["craft"]):
    return context.current_hero

  context = await go_to_workshop(context, desired["craft"]["skill"], db, action)  
  
  context = await action.hero.craft(context, desired["code"], qtty)

  return context


async def go_to_workshop(context, workshop_code, db, action):
  dest = await db.get_closest_map(context, content_type="workshop", content_code=workshop_code)
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    print(f"{context.current_hero.name} moves to {dest.x} {dest.y}")
    return await action.hero.move(context, dest.x, dest.y)
  return context
  