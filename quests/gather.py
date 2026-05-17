from helpers import check_bag_weight
from helpers.find_in_bag import find_in_bag
from routines import go_gather
from routines.go_deposit_items import go_deposit_items


class gather(quest):
    def __init__(self, item_code:str, quantity:int):
        super().__init__()
        self.item_code = item_code
        self.quantity = quantity
        
    async def run(self, context, town_hall, action, db):
        hero = context.current_hero
        in_pockets = find_in_bag(hero.inventory, self.item_code)
        if in_pockets >= self.quantity:
            print(f"[{hero.name}] already has {self.quantity} {self.item_code} in their bag.")
            context = await go_deposit_items(context, action, db, self.item_code, self.quantity)
            return "COMPLETED"
        
        if check_bag_weight(hero.inventory) + self.quantity > hero.inventory_max_items:
            print(f"[{hero.name}] can't carry {self.quantity} {self.item_code}. Need space !")
            context = await go_deposit_items(context, action, db, self.item_code, self.quantity)
            return "RUNNING" # On considère que le héros va faire de la place en déposant des items à la banque. On redemandera au prochain tick quoi faire.
        
        print(f"[{hero.name}] starts gathering {self.quantity} {self.item_code}...")
        context = await go_gather(context, action, db, self.item_code, self.quantity)
        return "RUNNING"