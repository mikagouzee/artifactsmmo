from controllers import ActionController, DbController
from helpers import can_survive, find_in_bag, check_location
from models import hero_context
from routines import go_equip


async def go_fight(context:hero_context, action:ActionController, db:DbController, monster_code=None):
  if find_in_bag(context.current_hero.inventory, "small_health_potion") < 0:
    context = await go_equip(context, "small_health_potion", action, db, slot="utility_1", quantity=20)
                
  
  if monster_code:
    monster = await db.monster.find_by_code(monster_code)  
    if not can_survive(context, monster):
      monster_code = await db.monster.get_best_monster(context.current_hero)

    dest = await db.get_closest_map(context, content_type="monster", content_code=monster_code)
    if dest and not check_location(context.current_hero, dest.x, dest.y):
      context = await action.hero.move(context, dest.x, dest.y)

    context = await heal(context, action, db)
      
    context = await action.hero.fight(context)
    
  return context


async def heal(context, action, db):
  if context.current_hero.hp < context.current_hero.max_hp:
    healing_stuff = [item for item in context.current_hero.inventory if item["code"] in db.item.food]
    if healing_stuff:
      best_healing_item = max(healing_stuff, key=lambda x: db.item.food[x["code"]])
      as_item = await db.item.find_by_code(best_healing_item["code"])
      qtty_to_consume = (context.current_hero.max_hp - context.current_hero.hp) // as_item["effects"][0]["value"] 
      if qtty_to_consume > 0:
        qtty_in_bag = find_in_bag(context.current_hero.inventory, best_healing_item["code"])
        qtty = min(qtty_in_bag, qtty_to_consume)
        context = await action.hero.use_item(context, best_healing_item["code"], qtty=qtty)
        context = await heal(context, action, db)
      else:
        return context
    elif context.current_hero.hp <= context.current_hero.max_hp /2:
      context = await action.hero.rest(context)
  return context