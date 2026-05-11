import asyncio
from controllers.action_controller import ActionController
from helpers.find_in_bag import check_bag_weight
from helpers.json_data_reader import read_json
from models import hero, item
from routines import go_craft, go_deposit_item, go_fight, go_gather


class farm_mining:
  def __init__(self, character: hero, controller:ActionController):
    self.my_hero = character
    self.controller = controller

  async def run(self):
    copper_bar_json = read_json("copper_bar.json")
    copper = item(**copper_bar_json)

    iron_bar_json = read_json("iron_bar.json")
    iron = item(**iron_bar_json)

    while True:
      if self.my_hero.mining_level < 10:
        self.my_hero = await go_gather(self.my_hero,self.controller, 'copper_rocks')      
        self.my_hero = await go_craft(self.my_hero, self.controller, copper, 'mining')
        self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      elif self.my_hero.mining_level < 20:
        self.my_hero = await go_gather(self.my_hero,self.controller, 'iron_rocks')      
        self.my_hero = await go_craft(self.my_hero, self.controller, iron, 'mining')
        self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      elif self.my_hero.mining_level < 30:
        self.my_hero = await go_gather(self.my_hero,self.controller, 'iron_rocks')      
        # self.my_hero = await go_craft(self.my_hero, self.controller, iron, 'mining')
        self.my_hero = await go_deposit_item(self.my_hero, self.controller)


