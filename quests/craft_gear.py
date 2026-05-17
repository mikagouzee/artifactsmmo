from helpers import find_in_bag
from routines import go_craft, go_deposit_items, go_withdraw_items


class craft_gear(quest):
    def __init__(self, target_item_code:str, quantity:int=1):
        super().__init__(name=f"Craft_{target_item_code}")
        self.target_item_code = target_item_code
        self.quantity = quantity

    async def run(self, context, town_hall, action, db):
        hero = context.current_hero
        #step 1 : analyse craft recipe
        item = await db.item.find_by_code(self.target_item_code)
        if not item or not item.get("craft"):
            print(f"Item {self.target_item_code} is not craftable or doesn't exist.")
            return "FAILED"
        
        ingredients_list = item["craft"]["items"]
        missing_group_wide = False
        needed_to_withdraw = []

        #step 2 : check stocks in bank and inventory
        for ingredient in ingredients_list:
            code = ingredient["code"]
            required_qty = ingredient["quantity"] * self.quantity

            in_inventory = find_in_bag(hero.inventory, code)
            in_bank = find_in_bag(await action.bank.get_bank_inventory(), code)
    
            total_available = in_inventory + in_bank

            if total_available < required_qty:
                missing_qty = required_qty - total_available
                town_hall.report_need(
                    item_code = code,
                    quantity = missing_qty,
                    priority=10, #high
                    requester = hero.name
                )
                missing_group_wide = True
                
            elif in_inventory < required_qty:
                 needed_to_withdraw.append({
                    "code":code,
                    "quantity":required_qty - in_inventory
                })
            
            if in_inventory < required_qty:
                needed_to_withdraw.append({
                    "code":code,
                    "quantity":required_qty - in_inventory
                })


        #step 3 : go craft or ask gatherer to farm missing items
        if missing_group_wide:
            print(f"[{hero.name}] Ressources manquantes pour {self.target_item_code}. S.O.S émis au TownHall.")
            # La quête échoue pour ce tick. Le GameRunner redemandera quoi faire au prochain tour.
            # Cela libère le crafteur pour autre chose en attendant que le récolteur livre.
            return "FAILED"

        # S'il faut retirer des objets de la banque
        if needed_to_withdraw:
            print(f"[{hero.name}] Déplacement à la banque pour récupérer les composants...")
            context = await go_withdraw_items(context, action, db, needed_to_withdraw)
            return "RUNNING"

        # 4. Exécution du craft (Tout est dans les poches)
        print(f"[{hero.name}] Tous les composants sont réunis. Lancement du craft...")
        context = await go_craft(context, action, db, item, self.quantity)

        # 5. Post-craft : On dépose l'item en banque pour que le Guerrier puisse le prendre
        print(f"[{hero.name}] Craft terminé. Dépôt de {self.target_item_code} à la banque pour l'équipe.")
        context = await go_deposit_items(context, action, db, self.target_item_code)

        return "COMPLETED"