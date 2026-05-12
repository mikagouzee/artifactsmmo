import asyncio
from controllers import ActionController, DbController
from helpers.json_data_reader import read_json
from managers.resource_manager import get_best_resource
from models import hero, item
from routines import go_gather, go_craft, go_deposit_item


class farm_alchemy:
  def __init__(self, character: hero, action:ActionController, db:DbController):
    self.my_hero = character
    self.action = action
    self.db = db
    
  async def run(self):
    
    while True:  
        target_code = await get_best_resource(self.my_hero.mining_level, "alchemy")
        self.my_hero = await go_gather(self.my_hero, self.action, self.db, target_code, 'apprentice_gloves')
        
        self.my_hero = await go_deposit_item(self.my_hero, self.controller)

      
        await asyncio.sleep(1)
      
      