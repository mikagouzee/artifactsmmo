from helpers import find_in_bag
from helpers.check_bag_weight import check_bag_weight
from routines import go_equip, go_fight, go_gather, go_get_new_task, go_deposit_items, go_deposit_gold, go_complete_task, go_produce, go_withdraw_items
from quests.quest import quest


class default_farm_quest(quest):
    def __init__(self):
        super().__init__(name="Default_Monster_Farm")

    async def run(self, context, town_hall, action, db) -> str:
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
                print(f"[{hero.name}] Progression Task :  {hero.task_progress}/{hero.task_total}. Récolte en cours...")
                #gotta check if it's craft or gather
                item = await db.item.find_by_code(hero.task)
                currently_hold = find_in_bag(hero.inventory, hero.task)
                needed = hero.task_total - hero.task_progress
                in_stock = town_hall.get_stock(hero.task)
                if in_stock + currently_hold >= needed:
                    context = await go_withdraw_items(context, action, db, [{"item":item, "quantity":in_stock}])
                    context = await go_complete_task(context, action, db)
                    return "RUNNING"

                if item["craft"]:
                    context = await go_produce(context, action, db, item)
                else:
                    source = await db.resource.get_resource_by_drop(hero.task)
                    context = await go_gather(context, action, db, source["code"])
                
                # context = await go_gather(context, action, db, source["code"])
                return "RUNNING"
        print(f"[{hero.name}] Task in-game complétée ! Validation au Task Master...")
        context = await go_complete_task(context, action, db)
        
        return "COMPLETED"
    

