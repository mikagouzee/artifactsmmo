from helpers import can_fulfill


class town_hall:
    def __init__(self, heroes):
        self.task_queue = []
        self.heroes = heroes
        self.resource_requests = []
        self.bank_cache = {}

    async def assign_quest(self, context, db):
        # Logic to assign a task to a hero
        hero = context.current_hero

        for index, request in enumerate(self.resource_requests):
            if await can_fulfill(hero, request, db):
                chosen_request = self.resource_requests.pop(index)
                print(f"[TownHall] Assigning {chosen_request['item_code']} x{chosen_request['quantity']} to {hero.name} (requested by {chosen_request['requester']})")
                from quests.gather_quest import gather_quest
                return gather_quest(chosen_request["item_code"], chosen_request["quantity"])
        
        return None  # No suitable quest found

    def report_need(self, item_code:str, quantity:int, priority:int, requester:str):
        """Les héros peuvent signaler un besoin de ressources via cette fonction."""
        for req in self.resource_requests:
            if req["item_code"] == item_code and req["requester"] == requester:
                req["quantity"] = max(req["quantity"], quantity)  # On garde la plus grande quantité demandée
                return
        self.resource_requests.append({"item_code": item_code, "quantity": quantity, "priority": priority, "requester": requester})
        self.resource_requests.sort(key=lambda x: x["priority"], reverse=True)  # Priorité décroissante

    async def create_quest(self, quest_type:str, details:dict):
        """Factory de quêtes basées sur le type et les détails."""
        pass
    