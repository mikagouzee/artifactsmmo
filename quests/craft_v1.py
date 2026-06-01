from helpers import check_quantity_in_bag, find_max_craftable_quantity
from helpers.craft import check_available_resources
from quests import quest
from routines import go_craft, go_deposit_items, go_withdraw_items
from townhall import town_hall


class craft_quest(quest):
    def __init__(self, target_item_code: str, quantity: int = 1):
        super().__init__(name=f"Craft_{target_item_code}")
        self.type = "craft"
        self.target = target_item_code
        self.quantity = quantity
        self.progress = 0
        self.step = "PREPARE"  # PREPARE → CRAFT → DEPOSIT → done

    async def run(self, context, action, db):
        hero = context.current_hero
        print(f"[{hero.name}] Running craft quest for {self.quantity}x {self.target}. Crafted so far: {self.progress}. Current step: {self.step}")
        item = await db.item.find_by_code(self.target)
        if not item or not item.get("craft"):
            print(f"Item {self.target} is not craftable or doesn't exist.")
            return "FAILED"

        if self.step == "DEPOSIT":
            context = await go_deposit_items(context, action, db, self.target)
            return "COMPLETED"

        recipe = item["craft"]
        ingredient_list = recipe["items"]
        items_per_craft = sum(i["quantity"] for i in ingredient_list)
        remaining_to_craft = self.quantity - self.progress

        # Calcul du craftable total (banque + sac)
        bank_inventory = await action.bank.get_bank_inventory() #["code":str, "quantity":int]
        in_pockets = [{ "code":item["code"] , "quantity":item["quantity"] } for item in context.current_hero.inventory]

        combined = check_available_resources(bank_inventory, in_pockets)
        total_craftable = find_max_craftable_quantity(combined, item)

        if total_craftable <= 0:
            for ingredient in ingredient_list:
                in_combined = check_quantity_in_bag(combined, ingredient["code"])
                if in_combined < ingredient["quantity"]:
                    await town_hall.report_need(
                        quest_type="gather",
                        target=ingredient["code"],
                        quantity=(ingredient["quantity"] * remaining_to_craft) - in_combined,
                        priority=10,
                        requester=hero.name,
                        assigned_to = None
                    )
            print(f"[{hero.name}] Not enough resources to craft any {self.target}. Reported needs for all ingredients.")
            return "FAILED"

        # Signale le manque pour ce qu'on ne peut pas encore faire
        if total_craftable < remaining_to_craft:
            shortfall = remaining_to_craft - total_craftable
            for ingredient in ingredient_list:
                await town_hall.report_need(
                    target=ingredient["code"],
                    quest_type="gather",
                    quantity=ingredient["quantity"] * shortfall,
                    priority=10,
                    requester=hero.name,
                    assigned_to = None
                )

        # Calcul du batch portable
        #TODO / Fix here : hero should at least take enough for some craft rather than fumble if the batch is too large
        available_space = hero.inventory_max_items - sum(x["quantity"] for x in hero.inventory)
        max_crafts_by_weight = available_space // items_per_craft

        if max_crafts_by_weight <= 0:
            # Sac plein d'autre chose, on vide d'abord
            context = await go_deposit_items(context, action, db)
            return "RUNNING"

        batch = min(remaining_to_craft, total_craftable, max_crafts_by_weight)

        # Retrait des ingrédients manquants
        needed_to_withdraw = []
        for ingredient in ingredient_list:
            total_needed = ingredient["quantity"] * batch
            in_pockets = check_quantity_in_bag(hero.inventory, ingredient["code"])
            amount_to_withdraw = max(0, total_needed - in_pockets)
            if amount_to_withdraw > 0:
                needed_to_withdraw.append({
                    "code": ingredient["code"],
                    "quantity": amount_to_withdraw
                })

        if needed_to_withdraw:
            context = await go_withdraw_items(context, action, db, needed_to_withdraw)
            return "RUNNING"

        # Craft
        context = await go_craft(context, action, db, item, batch)
        self.progress += batch

        if self.progress >= self.quantity:
            self.step = "DEPOSIT"  # prochain tick → dépôt

        return "RUNNING"