from controllers import ActionController, DbController
from helpers import check_bag_weight, find_in_bag, check_location, get_best_potion_in_stock, is_equipped
from models import hero_context
from routines import go_deposit_gold, go_deposit_items, go_equip, go_withdraw_items


async def go_prep_for_combat(context:hero_context, action:ActionController, db:DbController, monster):
  hero = context.current_hero
  #go_to_bank
  dest = await db.get_closest_map(context, content_type="bank", content_code="bank")
  if dest and not check_location(context.current_hero, dest.x, dest.y):
    print(f'Moving to the bank : {dest.x} {dest.y}')
    context = await action.hero.move(context, dest.x, dest.y)
  
  #deposit whatever
  if check_bag_weight(hero.inventory) == hero.inventory_max_items:
    print(f"[{hero.name}] Inventaire plein ! Passage à la banque.")
    context = await go_deposit_items(context, action, db)
    context = await go_deposit_gold(context, action, db)

  #check better equipment for given monster


  #grab potions
  bank_bag = await action.bank.get_bank_inventory()
  potions = db.item.healing_potions
  potion = get_best_potion_in_stock(context, bank_bag, potions)
  as_item = db.item.find_by_code(potion)
  if potion and not find_in_bag(context.current_hero, potion) and not is_equipped(context.current_hero, as_item):
    context = await go_equip(context, potion, action, db, quantity=10)
  
  return context


