import asyncio
from controllers.action_controller import ActionController
from helpers.find_in_bag import check_bag_weight
from helpers.json_data_reader import read_json
from models import hero, item
from routines import go_craft, go_deposit_item, go_fight


class farm_sheeps:
  def __init__(self, character: hero, controller:ActionController):
    self.my_hero = character
    self.controller = controller

  async def run(self):
    
    while True:
    
      self.my_hero = await go_fight(self.my_hero, "sheep", self.controller)
      self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      
      # elif self.my_hero.level <= 20:
      #   self.my_hero = await go_fight(self.my_hero, "green_slime", self.controller)
      #   self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      #give time to the API
      await asyncio.sleep(1)

