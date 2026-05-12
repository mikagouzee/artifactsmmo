import asyncio
from controllers import ActionController, DbController
from managers.resource_manager import get_best_resource
from models import hero
from routines import go_deposit_gold, go_gather, go_deposit_item


class farm:
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
        crt_level = getattr(self.my_hero, f"{self.skill}_level", 1)
        target_code = await get_best_resource(crt_level, self.skill)
        self.my_hero = await go_gather(self.my_hero, self.action, self.db, target_code)
        self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db)
        self.my_hero = await go_deposit_gold(self.my_hero, self.action, self.db)

      
        await asyncio.sleep(1)
      
      