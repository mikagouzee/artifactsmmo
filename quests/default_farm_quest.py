from helpers import find_in_bag
from helpers.check_bag_weight import check_bag_weight
from routines import go_fight, go_gather, go_get_new_task, go_deposit_items, go_deposit_gold, go_complete_task, go_produce, go_trade_task, go_withdraw_items
from quests.quest import quest
from townhall import town_hall


class default_farm_quest(quest):
    def __init__(self):
        super().__init__(name="Default_Monster_Farm")

    async def run(self, context, action, db) -> str:
        hero = context.current_hero
        
        if check_bag_weight(hero.inventory) == hero.inventory_max_items:
            print(f"[{hero.name}] Inventaire plein ! Passage à la banque.")
            context = await go_deposit_items(context, action, db)
            context = await go_deposit_gold(context, action, db)

        if not hero.task:
            print(f"[{hero.name}] Pas de task in-game. Récupération d'une task de monstres...")
            context = await go_get_new_task(context, action, db, task_type="monsters")
            return "RUNNING"
        
        if hero.task_progress < hero.task_total:
            if hero.task_type=="monsters":
                print(f"[{hero.name}] Progression Task : {hero.task_progress}/{hero.task_total}. Combat en cours...")
                #check if the hero has healing potions on him
                context = await go_fight(context, action, db, monster_code=hero.task)
                return "RUNNING"
            else:
                context = await self.manage_item_task(context, action, db)
                return "RUNNING"
               
        print(f"[{hero.name}] Task in-game complétée ! Validation au Task Master...")
        context = await go_complete_task(context, action, db)
        
        return "COMPLETED"
    

    async def manage_item_task(self, context, action, db):
        hero = context.current_hero
        print(f"[{hero.name}] Progression Task :  {hero.task_progress}/{hero.task_total}. Récolte en cours...")
        #gotta check if it's craft or gather
        item = await db.item.find_by_code(hero.task)
        currently_hold = find_in_bag(hero.inventory, hero.task)
        needed = hero.task_total - hero.task_progress
        # in_bank = await action.bank.get_bank_inventory()
        # in_stock = find_in_bag(in_bank, hero.task)

        from_cache = await town_hall.get_stock(hero.task)
        
        if currently_hold >= needed:
            context = await go_trade_task(context, action, db)
            return "RUNNING"
        elif from_cache:
            context = await go_withdraw_items(context, action, db, [{"item":item, "quantity":from_cache}])
            return "RUNNING"

        if item["craft"]:
            context = await go_produce(context, action, db, item)
        else:
            source = await db.resource.get_resource_by_drop(hero.task)
            context = await go_gather(context, action, db, source["code"])
        
        # context = await go_gather(context, action, db, source["code"])
        return context