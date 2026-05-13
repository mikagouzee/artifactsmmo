import asyncio
from controllers import ActionController, DbController
from helpers.find_in_bag import find_in_bag
from managers.item_manager import find_best_craft_item
from models import hero
from routines import go_craft, go_deposit_item, go_withdraw_items



class farm_craft:
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
        # crt_level = getattr(self.my_hero, f"{self.skill}_level", 1)
        bank_inventory = await self.action.get_bank_inventory(self.my_hero)
        target_item = await find_best_craft_item(self.my_hero, self.skill, bank_inventory)

        in_pockets = find_in_bag(self.my_hero, target_item[0]["craft"]["items"])
        if not in_pockets:
          self.my_hero = await go_withdraw_items(self.my_hero, self.action, self.db, target_item[0]["craft"]["items"])
        else:
          target_item[1] = target_item[1] - in_pockets

        self.my_hero = await go_craft(self.my_hero, self.action, self.db,target_item[0], self.skill)
        self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db, target_item.code)


      
        await asyncio.sleep(1)
      
      