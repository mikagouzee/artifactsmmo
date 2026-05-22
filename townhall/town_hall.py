from helpers import can_fulfill, find_in_bag
from controllers import action_controller, DbController


class town_hall:
    bank_cache:list             = []
    task_queue: list            = []
    resource_requests: list     = []
    db: DbController            = None
    action: action_controller   = None

    @staticmethod
    async def assign_quest(context, db):
        # Logic to assign a task to a hero
        hero = context.current_hero

        for index, request in enumerate(town_hall.resource_requests):
            if await can_fulfill(hero, request, db):
                chosen_request = town_hall.resource_requests.pop(index)
                print(f"[TownHall] Assigning {chosen_request['item_code']} x{chosen_request['quantity']} to {hero.name} (requested by {chosen_request['requester']})")
                from quests.gather import gather
                return gather(chosen_request["item_code"], chosen_request["quantity"])
        
        return None  # No suitable quest found

    @staticmethod
    async def report_need(item_code:str, quantity:int, priority:int, requester:str):
        """Les héros peuvent signaler un besoin de ressources via cette fonction."""
        qt = await town_hall.define_quest_type(item_code)

        for req in town_hall.resource_requests:
            if req["item_code"] == item_code and req["requester"] == requester:
                req["quantity"] = max(req["quantity"], quantity)  # On garde la plus grande quantité demandée
                return
            
        town_hall.resource_requests.append({"type":qt, "item_code": item_code, "quantity": quantity, "priority": priority, "requester": requester})
        town_hall.resource_requests.sort(key=lambda x: x["priority"], reverse=True)  # Priorité décroissante

    @staticmethod
    async def create_quest(quest_type:str, details:dict):
        """Factory de quêtes basées sur le type et les détails."""
        pass
    
    @staticmethod
    async def get_stock(item_code):
        if len(town_hall.bank_cache) < 1:
            town_hall.bank_cache = await town_hall.action.bank.get_bank_inventory()
        
        return find_in_bag(town_hall.bank_cache, item_code)
    
    @staticmethod
    async def define_quest_type(town_hall, item_code):
        item = await town_hall.db.item.find_by_code(item_code)

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