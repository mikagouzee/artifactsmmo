from helpers import check_bag_weight
from helpers.find_in_bag import find_in_bag
from routines import go_gather, go_produce
from routines.deposit_items import go_deposit_items
from .quest import quest

class job_quest(quest):
  def __init__(self, skill:str):
      super().__init__(f"Farm_{skill}")
      self.type = "job"
      self.target = skill
      
      
  async def run(self, context, town_hall, action, db):
      hero = context.current_hero

      skill_name = f'{self.skill}_level'

      item = await self.db.item.find_best_craft_item(hero, skill_name, False)
      if item:
        context = await go_produce(context, action, db, item)
        return "RUNNING"
      else:
        for ingredient in item["craft"]:
          await town_hall.report_need(ingredient["code"], ingredient["quantity"], 10, hero.name)
        return "FAILED"

  