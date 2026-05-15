import asyncio
from controllers import ActionController, DbController
from managers.resource_manager import get_best_resource
from models import hero
from routines import go_complete_task, go_deposit_gold, go_fight, go_gather, go_deposit_item, go_get_new_task, go_trade_task


class farm_task:
  def __init__(self, character: hero, action:ActionController, db:DbController, task_type:str="monsters" ):
    self.my_hero = character
    self.action = action
    self.db = db
    self.task_type = task_type

  async def run(self):
    if self.my_hero.task == None:
      self.my_hero = await go_get_new_task(self.my_hero, self.action, self.db, self.task_type) 
    
    match self.task_type:
      case "monsters":
        while self.my_hero.task_progress < self.my_hero.task_total:
          self.my_hero = await go_fight(self.my_hero, self.my_hero.task, self.action, self.db)

        self.my_hero = await go_complete_task(self.my_hero, self.action, self.db)

      case "items":
        while self.my_hero.task_progress < self.my_hero.task_total:
          self.my_hero = await go_gather(self.my_hero, self.action, self.db, self.my_hero.task)
          self.my_hero = await go_trade_task(self.my_hero, self.action, self.db)

    await asyncio.sleep(1)
  
      