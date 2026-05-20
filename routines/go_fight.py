from controllers import ActionController, DbController
from helpers import can_survive, find_in_bag, check_location
from models import hero_context


async def go_fight(context:hero_context, action:ActionController, db:DbController, monster_code=None):
  if monster_code:
    monster = await db.monster.find_by_code(monster_code)  
    if not can_survive(context.current_hero, monster):
      target_monster = await db.monster.get_best_monster(context.current_hero)
      monster_code = target_monster["code"]

    dest = await db.get_closest_map(context, content_type="monster", content_code=monster_code)
    if dest and not check_location(context.current_hero, dest.x, dest.y):
      context = await action.hero.move(context, dest.x, dest.y)

    context = await heal(context, action, db)
      
    context = await action.hero.fight(context)
    
  return context


async def heal(context, action, db):
  if context.current_hero.hp < context.current_hero.max_hp:
    healing_stuff = [item for item in context.current_hero.inventory if item["code"] in db.item.healing_items]
    if healing_stuff:
      best_healing_item = max(healing_stuff, key=lambda x: db.items.healing_items[x["code"]])
      qtty_to_consume = (context.current_hero.max_hp - context.current_hero.hp) // best_healing_item["effects"]["value"] 
      qtty_in_bag = find_in_bag(context.current_hero.inventory, best_healing_item["code"])
      qtty = min(qtty_in_bag, qtty_to_consume)
      context = await action.hero.use_item(context, best_healing_item["code"], qtty=qtty)
      context = await heal(context, action)
    elif context.current_hero.hp <= context.current_hero.max_hp /2:
      context = await action.hero.rest(context)
  return context