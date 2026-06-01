import asyncio
import time

from models import hero_context
from quests.default_farm_quest import default_quest
from quests.craft import craft_quest
from quests.gather import gather_quest
from quests.hunt import hunt_quest
from townhall import town_hall


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
        await town_hall.report_need(
            quest_type="craft",
            target="minor_health_potion",
            quantity=100,
            priority=99,
            requester="TEST_SYSTEM",
            assigned_to=None
        )

        while True:
            for context in self.hero_contexts:
                if getattr(context, 'next_action_time', 0) > time.time():
                    continue
                await self.progress_quest(context)

            await asyncio.sleep(1)

    def decide_next_quest(self, context):
        """Logique business : détermine la tâche à injecter."""
        hero = context.current_hero
        quest_log = context.quest_log
        current_quest = quest_log.get_current_quest()
        if current_quest:
            for request in town_hall.resource_requests:
                if request["priority"] > current_quest.priority:
                    print(
                        f"Interrupting {current_quest.name} for higher priority request: {request['type']} "
                        f"{request['target']} x{request['quantity']} (requested by {request['requester']})"
                    )
                    request["assigned_to"] = hero.name
                    # quest_log.push_next(self.create_quest_from_request(request))

        return default_quest()

    def create_quest_from_request(self, request):
        if request is None:
            return default_quest()

        match request["type"]:
            case "craft":
                return craft_quest(request["target"], request["quantity"])
            case "gather":
                return gather_quest(request["target"], request["quantity"])
            case "monster" | "hunt":
                return hunt_quest(request["target"], request["quantity"])
            case _:
                return default_quest()

    async def progress_quest(self, context: hero_context):
        hero = context.current_hero
        quest_log = context.quest_log

        if quest_log.is_empty:
            request = await town_hall.assign_quest(context, self.db)
            next_quest = self.create_quest_from_request(request) if request else self.decide_next_quest(context)
            quest_log.append_back(next_quest)

        current_quest = quest_log.get_current_quest()
        if current_quest:
            status = await current_quest.run(context, self.action, self.db)
            if status in ["COMPLETED", "FAILED"]:
                print(f"[{hero.name}] Quest {current_quest.name} ended with status: {status}")
                town_hall.release_request(current_quest.type, current_quest.target, hero.name)
                quest_log.pop_current()
            elif status == "RUNNING":
                print(f"[{hero.name}] Quest {current_quest.name} is still running ") #({current_quest.progress}/{current_quest.quantity}).
