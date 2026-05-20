from helpers import can_fulfill, find_in_bag
from controllers import action_controller, DbController

class town_hall:
    def __init__(self, heroes, db_controller:DbController, action_controller:action_controller):
        self.task_queue = []
        self.heroes = heroes
        self.resource_requests = []
        self.bank_cache = {}
        self.db = db_controller
        self.action = action_controller

    async def assign_quest(self, context, db):
        # Logic to assign a task to a hero
        hero = context.current_hero

        for index, request in enumerate(self.resource_requests):
            if await can_fulfill(hero, request, db):
                chosen_request = self.resource_requests.pop(index)
                print(f"[TownHall] Assigning {chosen_request['item_code']} x{chosen_request['quantity']} to {hero.name} (requested by {chosen_request['requester']})")
                from quests.gather import gather
                return gather(chosen_request["item_code"], chosen_request["quantity"])
        
        return None  # No suitable quest found

    async def report_need(self, item_code:str, quantity:int, priority:int, requester:str):
        """Les héros peuvent signaler un besoin de ressources via cette fonction."""
        qt = await self.define_quest_type(item_code)

        for req in self.resource_requests:
            if req["item_code"] == item_code and req["requester"] == requester:
                req["quantity"] = max(req["quantity"], quantity)  # On garde la plus grande quantité demandée
                return
            
        self.resource_requests.append({"type":qt, "item_code": item_code, "quantity": quantity, "priority": priority, "requester": requester})
        self.resource_requests.sort(key=lambda x: x["priority"], reverse=True)  # Priorité décroissante

    async def create_quest(self, quest_type:str, details:dict):
        """Factory de quêtes basées sur le type et les détails."""
        pass
    
    async def get_stock(self, item_code):
        if len(self.bank_cache) < 1:
            self.bank_cache = await self.action.bank.get_bank_inventory()
        
        return find_in_bag(self.bank_cache, item_code)
    
    async def define_quest_type(self, item_code):
        item = await self.db.item.find_by_code(item_code)

        if item.get("craft"):
            return "craft"
        
        match item["subtype"]:
            case "task":
                #go buy item from taskmaster
                return "task_buy"
            case "mob":
                #find from db monster that has item in loot
                return "monster"
            case _ : 
                return "gather"