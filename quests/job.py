from helpers import check_bag_weight
from routines import go_gather, go_produce
from routines.deposit_items import go_deposit_items
from .quest import quest

class job_quest(quest):
  def __init__(self, skill: str):
      super().__init__(f"Job_{skill}")
      self.type = "job"
      self.target = skill
      self.skill = skill
      self.target_level = None

  async def run(self, context, town_hall, action, db):
      hero = context.current_hero
      skill_name = f"{self.skill}_level"
      current_level = getattr(hero, skill_name, 0)
      target_level = ((current_level // 10) + 1) * 10
      self.target_level = target_level

      if current_level >= target_level:
          print(f"[{hero.name}] {self.skill} has reached the next job floor {target_level}.")
          return "COMPLETED"

      if check_bag_weight(hero.inventory) >= hero.inventory_max_items:
          print(f"[{hero.name}] Inventory full for job {self.skill}. Depositing first.")
          context = await go_deposit_items(context, action, db)
          return "RUNNING"

      bank_inventory = await action.bank.get_bank_inventory()
      candidate = await db.item.find_best_craft_item(hero, skill_name, bank_inventory, must_be_craftable=False)

      if candidate:
          item, craftable_qty = candidate
          if item and craftable_qty > 0:
              print(f"[{hero.name}] Job_{self.skill} will craft {item['code']} with {craftable_qty} possible.")
              context = await go_produce(context, action, db, item)
              return "RUNNING"

          if item:
              missing = self._missing_ingredients(item, bank_inventory, hero.inventory)
              if missing:
                  print(f"[{hero.name}] Missing resources to craft {item['code']}: {missing}")
                  for code, quantity in missing.items():
                      await town_hall.report_need(
                          quest_type="gather",
                          target=code,
                          quantity=quantity,
                          priority=10,
                          requester=hero.name,
                          assigned_to=None
                      )
                  return "FAILED"

      best_resource = await db.resource.get_best_resource(current_level, self.skill)
      if best_resource:
          print(f"[{hero.name}] No craftable job item found; gathering best resource {best_resource} for {self.skill}.")
          context = await go_gather(context, action, db, best_resource)
          return "RUNNING"

      print(f"[{hero.name}] No usable job target found for skill {self.skill}.")
      return "FAILED"

  def _missing_ingredients(self, item, bank_inventory, hero_inventory):
      combined = self._combine_resources(bank_inventory, hero_inventory)
      missing = {}
      for ingredient in item["craft"]["items"]:
          needed = ingredient["quantity"]
          held = combined.get(ingredient["code"], 0)
          if held < needed:
              missing[ingredient["code"]] = needed - held
      return missing

  def _combine_resources(self, bank_inventory, hero_inventory):
      combined = {item["code"]: item["quantity"] for item in (bank_inventory or [])}
      for inv_item in (hero_inventory or []):
          combined[inv_item["code"]] = combined.get(inv_item["code"], 0) + inv_item["quantity"]
      return combined

  