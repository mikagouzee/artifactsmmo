from helpers import check_bag_weight, check_quantity_in_bag
from helpers.combat import find_best_potion_in_stock
from helpers.inventory import check_is_equipped
from helpers.maps import check_location
from routines import go_gather
from routines.deposit_items import go_deposit_items
from routines.equip import go_equip
from routines.fight import go_fight
from townhall import town_hall
from .quest import quest

class hunt_quest(quest):
    def __init__(self, monster_code:str, quantity:int):
        super().__init__(f"HUNT_{quantity}_{monster_code}")
        self.target = monster_code
        self.type = "hunt"
        self.source = None
        self.target_quantity = quantity
        self.step = "HUNT"
        self.deposited = 0
        
    async def run(self, context, action, db):        
        if self.source is None: 
            self.source = await db.monster.find_by_code(self.target)
        
        if self.step == "GET_READY":    
          dest = await db.get_closest_map(context, content_type="bank", content_code="bank")
          
          if dest and not check_location(context.current_hero, dest.x, dest.y):
            print(f'Moving to the bank : {dest.x} {dest.y}')
            context = await action.hero.move(context, dest.x, dest.y)
          
            context = await self.get_potions(context, action, db)
            self.step = "HUNT"
        
            if self.hunted >= self.target_quantity:
                return "COMPLETED"
            return "RUNNING"

        if self.step == "HUNT":
          context = await go_fight(context, action, db, self.source["code"])
          
          return "RUNNING"
      
    async def get_potions(self, context, action, db):
      bank_bag = await action.bank.get_bank_inventory()
      potions = db.item.healing_potions
      potion = find_best_potion_in_stock(context, bank_bag, potions)
      if potion:
        as_item = await db.item.find_by_code(potion["code"])
        in_bag = check_quantity_in_bag(context.current_hero.inventory, potion)
        is_equipped = check_is_equipped(context.current_hero, as_item)
        
        if not in_bag or not is_equipped:
          context = await go_equip(context, as_item["code"], action, db, 'utility1', quantity=min(in_bag, 10))
      else:
        town_hall.report_need(
          quest_type="craft",
          target="small_health_potion", 
          quantity=500, 
          priority=99, 
          requester=context.current_hero.name,
          assigned_to = None)
      return context