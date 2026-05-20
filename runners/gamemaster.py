import asyncio
import time

from models import hero_context
from townhall import town_hall, default_farm_quest


class GameMaster:
    def __init__(self, action_controller, db_controller):
        self.action = action_controller
        self.db = db_controller
        self.hero_contexts = []


    async def initialize(self):
        # Liste de tes héros encapsulés dans leur contexte
        heroes = await self.action.get_all_heroes()
        self.hero_contexts = [hero_context(hero) for hero in heroes]
        self.town_hall = town_hall(heroes, self.db, self.action)

    async def run(self):
        """Boucle principale du bot."""
        await self.town_hall.report_need(
                    item_code="spruce_wood", 
                    quantity=100, 
                    priority=99, 
                    requester="TEST_SYSTEM"
                )

        while True:
            
            for context in self.hero_contexts:
                if getattr(context, 'next_action_time', 0) > time.time():
                    continue

                hero = context.current_hero
                queue = context.quest_log

                # 1. Si le héros n'a rien à faire, le Manager décide
                if queue.is_empty:
                    # C'est ici qu'on va lire le TownHall pour choisir la tâche
                    next_quest = await self.town_hall.assign_quest(context, self.db) or default_farm_quest()
                    queue.append_back(next_quest)

                # 2. On récupère la tâche en cours et on l'exécute
                current_quest = queue.get_current_quest()
                if current_quest:
                    status = await current_quest.run(context, self.town_hall, self.action, self.db)

                    # 3. Si la tâche est finie, on la dégage de la queue
                    if status in ["COMPLETED", "FAILED"]:
                        print(f"Quest {current_quest.name} of {hero.name} ended with status: {status}")
                        queue.pop_current()

            # Pause globale entre deux vérifications de l'équipe (ex: 1 seconde)
            await asyncio.sleep(1)

    def decide_next_task(self, context):
        """Logique business : détermine la tâche à injecter."""
        # Pour l'instant, on retourne une tâche "Default" basique
        return default_farm_quest()
    