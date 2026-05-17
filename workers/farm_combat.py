import asyncio
from controllers import ActionController, DbController

from helpers import check_bag_weight
from managers import monster_manager
from models import hero
from routines import go_deposit_items, go_fight, go_deposit_gold


class farm_combat:
  def __init__(self, character: hero, action:ActionController, db:DbController, monster_code:str=None):
    self.my_hero = character
    self.action = action
    self.db = db
    self.monster_code = monster_code

  async def run(self):
    # cooked_chicken_json=read_json("cooked_chicken.json")
    # cooked_chicken = item(**cooked_chicken_json)
    max_weight = self.my_hero.inventory_max_items
    while True:
      if check_bag_weight(self.my_hero.inventory) == max_weight:
        self.my_hero = await go_deposit_items(self.my_hero, self.action, self.db)
        self.my_hero = await go_deposit_gold(self.my_hero, self.action, self.db)
        continue
      
      
      
      self.my_hero = await go_fight(self.my_hero, target_monster, self.action, self.db)
      
      #give time to the API
      await asyncio.sleep(1)

