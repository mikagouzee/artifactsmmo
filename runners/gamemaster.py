import asyncio
import time
from models import hero_context
from quests import default_farm_quest
from townhall import town_hall
from quests.gather import gather_quest


class GameMaster:
    def __init__(self, action_controller, db_controller):
        self.action = action_controller
        self.db = db_controller
        self.hero_contexts = []

    async def initialize(self):
        # Liste de tes héros encapsulés dans leur contexte
        heroes = await self.action.get_all_heroes()
        self.hero_contexts = [hero_context(hero, self.db.item) for hero in heroes]

    async def run(self):
        """Main Bot loop."""
        # town_hall.create_quest("farm_skill")
        await town_hall.report_need(
                    quest_type="craft",
                    target="small_health_potion", 
                    quantity=100, 
                    priority=99, 
                    requester="TEST_SYSTEM",
                    assigned_to = None
                )
        
        # await town_hall.report_need(
        #             quest_type="gather",
        #             target="iron_ore", 
        #             quantity=100, 
        #             priority=99, 
        #             requester="TEST_SYSTEM",
        #             assigned_to = None
        #         )

        while True:            
            for context in self.hero_contexts:
               if getattr(context, 'next_action_time', 0) > time.time():
                    continue
               await self.progress_quest(context)

            for quest in town_hall.resource_requests:
                print(f"Pending request: {quest['type']} {quest['target']} x{quest['quantity']} (requested by {quest['requester']}, assigned to {quest['assigned_to']})")

            # Pause globale entre deux vérifications de l'équipe (ex: 1 seconde)
            await asyncio.sleep(1)



    def decide_next_quest(self, context):
        """Logique business : détermine la tâche à injecter."""
        # jobs = [{key:value} for (key, value) in context.current_hero.__dict__ if key.endwith('_level')]
        
        # for job in job:

        return default_farm_quest()
        # return gather_quest("sunflower", 100)
    

    async def progress_quest(self, context:hero_context):
        hero = context.current_hero
        quest_log = context.quest_log

        if quest_log.is_empty:
            next_quest = await town_hall.assign_quest(context, self.db) or self.decide_next_quest(context)
            quest_log.append_back(next_quest)

        current_quest = quest_log.get_current_quest()
        if current_quest:
            status = await current_quest.run(context, self.action, self.db)

            if status in ["COMPLETED", "FAILED"]:
                print(f"Quest {current_quest.name} of {hero.name} ended with status: {status}")
                town_hall.release_request(current_quest.type, current_quest.target, hero.name)
                quest_log.pop_current()