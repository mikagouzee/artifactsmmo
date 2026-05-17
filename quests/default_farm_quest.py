from helpers.check_bag_weight import check_bag_weight
from routines import go_fight, go_get_new_task, go_deposit_items, go_deposit_gold, go_complete_task
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
        
        # 2. Si le héros n'a pas de quête officielle (In-game task)
        if hero.task is None:
            print(f"[{hero.name}] Pas de task in-game. Récupération d'une task de monstres...")
            # Ton ancien worker adapté : doit accepter 'context', faire l'appel API, 
            # appeler 'process_result(response, context)' et retourner le context mis à jour.
            context = await go_get_new_task(context, action, db, task_type="monsters")
            return "RUNNING"

        # 3. Si la quête officielle est en cours, on fait UN combat
        if hero.task_progress < hero.task_total:
            print(f"[{hero.name}] Progression Task : {hero.task_progress}/{hero.task_total}. Combat en cours...")
            # Ton ancienne routine de combat adaptée : fait UN UNIQUE combat,
            # gère le process_result/cooldown, et met à jour le contexte.
            context = await go_fight(context, action, db)
            return "RUNNING"

        # 4. Si la quête officielle est terminée, on va la valider auprès du PNJ
        print(f"[{hero.name}] Task in-game complétée ! Validation au Task Master...")
        context = await go_complete_task(context, action, db)
        
        # Notre Quest de bot est maintenant arrivée à son terme avec succès
        return "COMPLETED"