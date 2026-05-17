import asyncio
from controllers import ActionController, DbController
from controllers.managers.resource_manager import get_best_resource
from models import hero
from routines import go_deposit_gold, go_gather, go_deposit_items


class farm:
  def __init__(self, character: hero, action:ActionController, db:DbController, skill:str, target_level:int=None, resource_code:str=None):
    self.my_hero = character
    self.action = action
    self.db = db
    self.skill = skill
    skillName = self.skill + "_level"
    crt_level = getattr(self.my_hero, skillName, 1)
    self.target_level = target_level if target_level else crt_level+10
    self.resource_code = resource_code

  async def run(self):
    
    while True:  
        if self.resource_code == None:
          crt_level = getattr(self.my_hero, f"{self.skill}_level", 1)
          target_code = await get_best_resource(crt_level, self.skill)
        else:
          target_code = self.resource_code
          
        self.my_hero = await go_gather(self.my_hero, self.action, self.db, target_code)
        self.my_hero = await go_deposit_items(self.my_hero, self.action, self.db)
        self.my_hero = await go_deposit_gold(self.my_hero, self.action, self.db)

      
        await asyncio.sleep(1)
      
      