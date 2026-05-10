import asyncio
from controllers.action_controller import ActionController
from helpers.json_data_reader import read_json
from models import hero, item
from routines import go_gather, go_craft, go_deposit_item


class farm_alchemy:
  def __init__(self, character: hero, controller:ActionController):
    self.my_hero = character
    self.controller = controller
    
  async def run(self):

    shp_json = read_json("small_health_potion.json")
    shp = item(**shp_json)
    
    while True:  
      if (self.my_hero.alchemy_level < 16):
        self.my_hero = await go_gather(self.my_hero, self.controller, 'sunflower_field', 'apprentice_gloves')
        
        self.my_hero = await go_craft(self.my_hero, self.controller, shp, shp.craft.skill)

        self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      
      elif (self.my_hero.alchemy_level < 21):
        self.my_hero = await go_gather(self.my_hero, self.controller, 'gudgeon_spot', 'fishing_net')
        # self.my_hero = await go_gather(self.my_hero, self.controller, 'nettle', 'apprentice_gloves')
        # self.my_hero = await go_craft(self.my_hero, self.controller, shp, 'alchemy')

        self.my_hero = await go_deposit_item(self.my_hero, self.controller)
      #give time to the API
      await asyncio.sleep(1)
      
      