from helpers.check_bag_weight import check_bag_weight
from routines import go_fight, go_gather, go_get_new_task, go_deposit_items, go_deposit_gold, go_complete_task
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
                context = await go_fight(context, action, db, monster_code=hero.task)
                return "RUNNING"
            else:
                print(f"[{hero.name}] Progression Task :  {hero.task_progress}/{hero.task_total}. Récolte en cours...")
                #gotta check if it's craft or gather
                # source = await db.resource.get_resource_name_by_drop(hero.task)
                # context = await go_gather(context, action, db, source["code"])
                return "RUNNING"
        print(f"[{hero.name}] Task in-game complétée ! Validation au Task Master...")
        context = await go_complete_task(context, action, db)
        
        return "COMPLETED"