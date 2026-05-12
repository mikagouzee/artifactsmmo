import asyncio
from controllers import ActionController, DbController
from models import hero
from routines import go_deposit_item, go_fight


class farm_sheeps:
  def __init__(self, character: hero, action:ActionController, db:DbController):
    self.my_hero = character
    self.action = action
    self.db = db

  async def run(self):
    
    while True:
    
      self.my_hero = await go_fight(self.my_hero, "sheep", self.action, self.db)
      self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db)
      
      # elif self.my_hero.level <= 20:
      #   self.my_hero = await go_fight(self.my_hero, "green_slime", self.controller)
      #   self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      #give time to the API
      await asyncio.sleep(1)

