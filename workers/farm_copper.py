import asyncio
from controllers.action_controller import ActionController
from helpers.json_data_reader import read_json
from models import hero, item
from routines import go_gather, go_craft, go_deposit_item


class farm_copper:
  def __init__(self, character: hero, controller:ActionController):
    self.my_hero = character
    self.controller = controller

  async def run(self):
    copper_bar_json = read_json("copper_bar.json")
    copper = item(**copper_bar_json)
    while True:  
      #this is the "long step", as one gather takes 30sec, -10% thanks to the pickaxe
      #We can gather approximately 100 copper -> 100 * 27 sec -> 45min
      self.my_hero = await go_gather(self.my_hero,self.controller, 'copper_rocks')
      
      # self.my_hero = await go_craft(self.my_hero, self.controller, copper, 'mining')

      #this is also very fast, as we deposit approximately 9-10 bars for a total of 40 sec cooldown
      self.my_hero = await go_deposit_item(self.my_hero, self.controller)

      #give time to the API
      await asyncio.sleep(1)