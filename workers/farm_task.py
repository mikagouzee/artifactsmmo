import asyncio
from controllers import ActionController, DbController
from helpers import find_in_bag, find_max_craftable_quantity
from controllers.managers.item_manager import find_item_by_code
from controllers.managers.resource_manager import get_resource_name_by_drop
from models import hero
from routines import go_complete_task, go_deposit_gold, go_fight, go_gather, go_deposit_items, go_get_new_task, go_produce, go_trade_task, go_withdraw_items


class farm_task:
  def __init__(self, character: hero, action:ActionController, db:DbController, task_type:str="monsters" ):
    self.my_hero = character
    self.action = action
    self.db = db
    self.task_type = character.task_type if character.task_type else task_type

  async def run(self):
    if not self.my_hero.task:
      self.my_hero = await go_get_new_task(self.my_hero, self.action, self.db, self.task_type) 

    while self.my_hero.task_progress < self.my_hero.task_total:
      match self.task_type:
        case "monsters":
            self.my_hero = await go_fight(self.my_hero, self.my_hero.task, self.action, self.db)

        case "items":
            desired = await find_item_by_code(self.my_hero.task)

            if desired["craft"] is None:
              self.my_hero = await self.try_get_from_bank(self.my_hero.task)
              self.my_hero = await go_gather(self.my_hero, self.action, self.db, self.my_hero.task)
              self.my_hero = await go_trade_task(self.my_hero, self.action, self.db)

            else:
              bank_items = await self.action.get_bank_inventory()

              while find_max_craftable_quantity(bank_items, desired) > 0:
                self.my_hero = await go_produce(self.my_hero, self.action, self.db, desired)
                self.my_hero = await go_trade_task(self.my_hero, self.action, self.db)
                bank_items = await self.action.get_bank_inventory()
              else:
                #will work as long as there's a single item needed for the craft
                #! the craft gives the name of the RESOURCE gathered;
                resource_to_gather = await get_resource_name_by_drop(desired["craft"]["items"][0]["code"])
                quantity = sum([item["quantity"] for item in desired["craft"]["items"]])
                while find_in_bag(self.my_hero.inventory, resource_to_gather) <= quantity * desired["craft"]["quantity"]:
                  self.my_hero = await go_gather(self.my_hero, self.action, self.db, resource_to_gather["code"])
                  self.my_hero = await go_produce(self.my_hero, self.action, self.db, desired)

    self.my_hero = await go_complete_task(self.my_hero, self.action, self.db)
    #accept new task ? 

    await asyncio.sleep(1)
  
  
  async def try_get_from_bank(self, target_item):
    bank_items = await self.action.get_bank_inventory()
    in_bank = find_in_bag(bank_items, self.my_hero.task)
    if in_bank > 0:
      return await go_withdraw_items(self.my_hero, self.action, self.db, [{"code":self.my_hero.task,"quantity":in_bank}])
    return self.my_hero
    