import asyncio
from controllers import ActionController, DbController
from managers.resource_manager import get_best_resource
from models import hero
from routines import go_deposit_item, go_gather


class farm_mining:
  def __init__(self, character: hero, action:ActionController,db:DbController, target_level:int):
    self.my_hero = character
    self.action = action
    self.db = db
    self.target_level = target_level if target_level else self.my_hero.mining_level+10

  async def run(self):
    
    while self.my_hero.mining_level < self.target_level:
      target_code = await get_best_resource(self.my_hero.mining_level, "mining")
      self.my_hero = await go_gather(self.my_hero, self.action, self.db, target_code)
      self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db)
      await asyncio.sleep(1)

    return self.my_hero
      # if self.my_hero.mining_level <= 10:
      #   self.my_hero = await go_gather(self.my_hero,self.controller, 'copper_rocks')      
      #   self.my_hero = await go_craft(self.my_hero, self.controller, copper, 'mining')
      #   self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      # elif self.my_hero.mining_level <= 20:
      #   self.my_hero = await go_gather(self.my_hero,self.controller, 'iron_rocks')      
      #   self.my_hero = await go_craft(self.my_hero, self.controller, iron, 'mining')
      #   self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      # elif self.my_hero.mining_level <= 30:
      #   self.my_hero = await go_gather(self.my_hero,self.controller, 'coal_rocks')      
      #   # self.my_hero = await go_craft(self.my_hero, self.controller, iron, 'mining')
      #   self.my_hero = await go_deposit_item(self.my_hero, self.controller)


