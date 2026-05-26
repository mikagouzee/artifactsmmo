from controllers import ActionController, DbController
from helpers import check_location
from models import hero
from models.hero_context import hero_context


async def go_deposit_gold(context:hero_context,action:ActionController,db:DbController):
  print(f'{context.current_hero.name} will now deposit {context.current_hero.gold} gold to the bank!')

  if context.current_hero.gold < 1:
    return context
  
  dest = await db.get_closest_map(context, content_type="bank", content_code="bank")
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    print(f'Moving to the bank : {dest.x} {dest.y}')
    context = await action.hero.move(context, dest.x, dest.y)
    
  context = await action.bank.deposit_gold(context)

  return context