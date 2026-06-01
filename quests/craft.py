from helpers.craft import check_available_resources, check_quantity_in_bag
from quests import quest
from routines.craft import go_craft
from routines.deposit_items import go_deposit_items
from routines.withdraw_items import go_withdraw_items
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
            await go_deposit_items(context, action, db, self.target)
            return "COMPLETED"


        recipe = item["craft"]
        ingredient_list = recipe.get("items", [])
        if not ingredient_list:
            print(f"Craft recipe for {self.target} has no ingredient list.")
            return "FAILED"

        remaining_output = max(0, self.quantity - self.progress)
        bank_inventory = await action.bank.get_bank_inventory()
        combined_inventory = check_available_resources(bank_inventory, hero.inventory)

        max_ops = self._max_craft_operations(combined_inventory, recipe)
        if max_ops <= 0:
            await self._report_missing_ingredients(hero, combined_inventory, ingredient_list, remaining_output)
            return "FAILED"

        output_per_op = recipe.get("quantity", 1)
        required_ops = self._ops_needed_for_output(remaining_output, output_per_op)
        if required_ops <= 0:
            self.step = "DEPOSIT"
            return "RUNNING"

        if max_ops < required_ops:
            await self._report_missing_ingredients(hero, combined_inventory, ingredient_list, remaining_output)

        batch_ops = min(required_ops, max_ops)
        batch_ops = self._limit_batch_by_slot_capacity(context, recipe, batch_ops)

        if batch_ops <= 0:
            if await self._deposit_non_ingredient_items(context, action, db, ingredient_list):
                return "RUNNING"
            print(f"[{hero.name}] Not enough inventory capacity to prepare ingredients for crafting {self.target}.")
            return "FAILED"

        if await self._withdraw_missing_ingredients(context, action, db, ingredient_list, batch_ops):
            return "RUNNING"

        context = await go_craft(context, action, db, item, batch_ops)
        self.progress += batch_ops * output_per_op

        if self.progress >= self.quantity:
            self.step = "DEPOSIT"

        return "RUNNING"

    def _max_craft_operations(self, combined_inventory, recipe):
        operations = float("inf")
        for ingredient in recipe.get("items", []):
            available_qty = check_quantity_in_bag(combined_inventory, ingredient["code"])
            operations = min(operations, available_qty // ingredient.get("quantity", 1))

        return int(operations) if operations != float("inf") else 0

    def _ops_needed_for_output(self, remaining_output, output_per_op):
        if remaining_output <= 0:
            return 0
        return (remaining_output + output_per_op - 1) // output_per_op

    async def _report_missing_ingredients(self, hero, combined_inventory, ingredient_list, remaining_output):
        output_per_op = 1
        required_ops = self._ops_needed_for_output(remaining_output, output_per_op)

        for ingredient in ingredient_list:
            required_qty = ingredient["quantity"] * required_ops
            current_qty = check_quantity_in_bag(combined_inventory, ingredient["code"])
            if current_qty < required_qty:
                missing_qty = required_qty - current_qty
                await town_hall.report_need(
                    quest_type="gather",
                    target=ingredient["code"],
                    quantity=missing_qty,
                    priority=10,
                    requester=hero.name,
                    assigned_to=None
                )

    def _limit_batch_by_slot_capacity(self, context, recipe, batch_ops):
        hero = context.current_hero
        free_space = hero.inventory_max_items - sum(item["quantity"] for item in hero.inventory)

        while batch_ops > 0:
            required_withdraw = self._withdraw_qty_for_batch(hero.inventory, recipe.get("items", []), batch_ops)
            if required_withdraw <= free_space:
                break
            batch_ops -= 1

        return batch_ops

    def _withdraw_qty_for_batch(self, inventory, ingredient_list, batch_ops):
        withdraw_qty = 0
        for ingredient in ingredient_list:
            required_qty = ingredient["quantity"] * batch_ops
            current_qty = check_quantity_in_bag(inventory, ingredient["code"])
            withdraw_qty += max(0, required_qty - current_qty)
        return withdraw_qty

    async def _deposit_non_ingredient_items(self, context, action, db, ingredient_list):
        ingredient_codes = {item["code"] for item in ingredient_list}
        deposited = False
        for inventory_item in list(context.current_hero.inventory):
            if inventory_item["code"] not in ingredient_codes:
                context = await go_deposit_items(context, action, db, inventory_item["code"])
                deposited = True
        return deposited

    async def _withdraw_missing_ingredients(self, context, action, db, ingredient_list, batch_ops):
        missing_items = []
        for ingredient in ingredient_list:
            required_qty = ingredient["quantity"] * batch_ops
            current_qty = check_quantity_in_bag(context.current_hero.inventory, ingredient["code"])
            if current_qty < required_qty:
                missing_items.append({
                    "code": ingredient["code"],
                    "quantity": required_qty - current_qty
                })

        if not missing_items:
            return False

        await go_withdraw_items(context, action, db, missing_items)
        return True
