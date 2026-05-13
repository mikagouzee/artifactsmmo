import asyncio
from controllers import ActionController, DbController
from helpers import check_bag_weight
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
        item_and_iteration = await find_best_craft_item(self.my_hero, self.skill, bank_inventory)
        if not item_and_iteration:
          print(f"You can no longer progress in that craft for now")
          return self.my_hero

        ingredient_list = item_and_iteration[0]["craft"]["items"]
        total_craft_possible = item_and_iteration[1]

        available_space = self.my_hero.inventory_max_items - check_bag_weight(self.my_hero.inventory)

        items_per_craft = sum(a["quantity"] for a in ingredient_list)

        max_crafts_by_weight = available_space // items_per_craft

        can_carry = min(total_craft_possible, max_crafts_by_weight)

        if can_carry <= 0:
          break

        needed_items = []
        for ingredient in ingredient_list:
          total_needed = ingredient["quantity"] * can_carry
        
          in_pockets = find_in_bag(self.my_hero.inventory, ingredient["code"])
          amount_to_withdraw = max(0, total_needed - in_pockets)

          if amount_to_withdraw > 0:
            needed_items.append({
              "code":ingredient["code"],
              "quantity":amount_to_withdraw
            })

        self.my_hero = await go_withdraw_items(self.my_hero, self.action, self.db, needed_items)       
        self.my_hero = await go_craft(self.my_hero, self.action, self.db,item_and_iteration[0], self.skill, can_carry)
        self.my_hero = await go_deposit_item(self.my_hero, self.action, self.db)
      
        await asyncio.sleep(1)
      
      