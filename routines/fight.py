from controllers import ActionController, DbController
from helpers import can_survive, check_location, find_best_monster
from helpers.combat import heal
from models import hero_context


async def go_fight(context:hero_context, action:ActionController, db:DbController, monster_code=None):
  if monster_code:
    monster = await db.monster.find_by_code(monster_code)  
    if not can_survive(context, monster):
      possible_monsters = await db.monster.get_candidates(context)
      monster_code = find_best_monster(context, possible_monsters)

    dest = await db.get_closest_map(context, content_type="monster", content_code=monster_code)
    if dest and not check_location(context.current_hero, dest.x, dest.y):
      context = await action.hero.move(context, dest.x, dest.y)

    context = await heal(context, action, db)
      
    context = await action.hero.fight(context)
    
  return context

