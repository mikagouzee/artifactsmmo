from helpers import check_bag_weight
from helpers.find_in_bag import find_in_bag
from routines import go_gather
from routines.go_deposit_items import go_deposit_items
from .quest import quest

class gather(quest):
    def __init__(self, item_code:str, quantity:int):
        super().__init__(f"GATHER_{quantity}_{item_code}")
        self.item_code = item_code
        self.source = ''
        self.target_quantity = quantity
        
    async def run(self, context, town_hall, action, db):
        hero = context.current_hero
        self.source = await db.resource.get_resource_by_drop(self.item_code)

        total_available = await town_hall.get_stock(self.item_code) + find_in_bag(hero.inventory, self.item_code)
        if total_available >= self.target_quantity:
            return "COMPLETED"
        
        in_pockets = find_in_bag(hero.inventory, self.item_code)

        if in_pockets >= self.target_quantity:
            context = await go_deposit_items(context, action, db, self.item_code, self.target_quantity)
            return "COMPLETED"
        
        if check_bag_weight(hero.inventory) + self.target_quantity > hero.inventory_max_items:
            context = await go_deposit_items(context, action, db)
            return "RUNNING" # On considère que le héros va faire de la place en déposant des items à la banque. On redemandera au prochain tick quoi faire.
        
        context = await go_gather(context, action, db, self.source["code"])
        return "RUNNING"