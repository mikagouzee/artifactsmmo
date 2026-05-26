from helpers import check_bag_weight, check_quantity_in_bag
from routines import go_gather
from routines.deposit_items import go_deposit_items
from .quest import quest

class gather_quest(quest):
    def __init__(self, item_code:str, quantity:int):
        super().__init__(f"GATHER_{quantity}_{item_code}")
        self.target = item_code
        self.type = "gather"
        self.source = None
        self.target_quantity = quantity
        self.step = "GATHER"
        self.deposited = 0
        
    async def run(self, context, action, db):
        hero = context.current_hero
        
        if self.source is None: 
            self.source = await db.resource.get_resource_by_drop(self.target)
        
        if self.step == "DEPOSIT":    
            in_pockets = check_quantity_in_bag(hero.inventory, self.target)
            context = await go_deposit_items(context, action, db, self.target)
            self.deposited += in_pockets
            self.step = "GATHER"
        
            if self.deposited >= self.target_quantity:
                return "COMPLETED"
            return "RUNNING"

        in_pockets = check_quantity_in_bag(hero.inventory, self.target)
        bag_full = check_bag_weight(hero.inventory) >= hero.inventory_max_items

        if in_pockets + self.deposited >= self.target_quantity or bag_full:
            self.step = "DEPOSIT"
            return "RUNNING"
        
        context = await go_gather(context, action, db, self.source["code"])
        return "RUNNING"