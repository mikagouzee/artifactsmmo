from controllers import ActionController, DbController
from helpers import find_in_bag, check_location
from models import hero_context


async def go_fight(context:hero_context, action:ActionController, db:DbController, monster_code=None):
  if monster_code is None:
    target_monster = await db.monster.get_best_monster(context.current_hero)
  else:
    target_monster = monster_code
  
  dest = await db.get_closest_map(context, content_type="monster", content_code=target_monster)
  
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    context = await action.hero.move(context, dest.x, dest.y)

  if context.current_hero.hp < context.current_hero.max_hp:
    if find_in_bag(context.current_hero.inventory, 'cooked_chicken') > 0:
      context = await action.hero.use_item(context, 'cooked_chicken')
    elif context.current_hero.hp <= context.current_hero.max_hp /2:
      context = await action.hero.rest(context)
    else:        
      if dest and not check_location(context.current_hero, dest.x, dest.y):
        context = await action.hero.move(context, dest.x, dest.y)
        
      context = await action.hero.fight(context)
  else:
    if dest and not check_location(context.current_hero, dest.x, dest.y):
      context = await action.hero.move(context, dest.x, dest.y)
    context = await action.hero.fight(context)

  return context