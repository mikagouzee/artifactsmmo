import asyncio
from controllers import ActionController, DbController
from managers.item_manager import find_best_craft_item
from models import hero
from routines import go_craft, go_deposit_item



class farm_Craft:
  def __init__(self, character: hero, action:ActionController, db:DbController, skill:str, target_level:int=None):
    self.my_hero = character
    self.action = action
    self.db = db
    self.skill = skill
    skillName = self.skill + "_level"
    crt_level = getattr(self.my_hero, skillName, 1)
    self.target_level = target_level if target_level else crt_level+10

  async def run(self):
    
    while True:  
        crt_level = getattr(self.my_hero, f"{self.skill}", 1)
        bank_inventory = await self.action.get_bank_inventory(self.my_hero)
        target_item = await find_best_craft_item(crt_level, self.skill, bank_inventory)
        self.my_hero = await go_withdraw(self.my_hero, self.action, self.db, target_item.craft.ingredients)
        self.my_hero = await go_craft(target_item, self.my_hero, self.action, self.db, self.skill)
        self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db, target_item.code)


      
        await asyncio.sleep(1)
      
      