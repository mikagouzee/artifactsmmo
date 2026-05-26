
from controllers import ActionController, db_controller
from helpers import check_quantity_in_bag, check_location
from models import hero
from townhall import town_hall


async def go_equip(context, item_code, action:ActionController,db:db_controller, slot="weapon", quantity=1):
  slot_name = f'{slot}_slot'
  if context.current_hero.getattr(slot_name) == item_code:
    return context

  if check_quantity_in_bag(context.current_hero.inventory, item_code):
    print(f'{context.current_hero.name} found {item_code} !.')
    context = await action.hero.equip(context, item_code, slot=slot, qtty=quantity)
  else:
    dest = await db.get_closest_map(context, content_code='bank', content_type='bank')
    if dest and not check_location(context.current_hero, dest.x, dest.y):
      context = await action.hero.move(context, dest.x, dest.y)  
    context = await action.bank.withdraw(context, item_code, quantity)

    if check_quantity_in_bag(context.current_hero.inventory, item_code):
      context = await action.hero.equip(context, item_code, slot=slot, qtty=quantity)
    else:
        await town_hall.report_need(
                    quest_type="craft",
                    target="small_health_potion", 
                    quantity=200, 
                    priority=99, 
                    requester=context.current_hero.name,
                    assigned_to = None)

  return context