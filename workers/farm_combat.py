import asyncio
from controllers import ActionController, DbController

from models import hero
from routines import go_craft, go_deposit_item, go_fight


class farm_combat:
  def __init__(self, character: hero, action:ActionController, db:DbController):
    self.my_hero = character
    self.action = action
    self.db = db

  async def run(self):
    # cooked_chicken_json=read_json("cooked_chicken.json")
    # cooked_chicken = item(**cooked_chicken_json)
    while True:
      if self.my_hero.level <= 5:
        self.my_hero = await go_fight(self.my_hero, "chicken", self.action, self.db)
        # self.my_hero = await go_craft(self.my_hero, self.controller, cooked_chicken, 'cooking')
        self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db)
      elif self.my_hero.level <= 11: 
        self.my_hero = await go_fight(self.my_hero, "yellow_slime", self.action, self.db)
        #self.my_hero = await go_craft(self.my_hero, self.controller, cooked_chicken, 'cooking')
        self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db)
      elif self.my_hero.level <= 18:
        self.my_hero = await go_fight(self.my_hero, "red_slime", self.action, self.db)
        self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db)
      #give time to the API
      await asyncio.sleep(1)

