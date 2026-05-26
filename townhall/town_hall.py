from helpers import can_fulfill, check_quantity_in_bag
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
            if request["assigned_to"] is not None:
                continue
            if await can_fulfill(context, request, db):
                # chosen_request = town_hall.resource_requests.pop(index)
                request["assigned_to"] = context.current_hero.name
                match request["type"] :
                    case "craft":
                        from quests.craft import craft_quest
                        return craft_quest(request["target"], request["quantity"])
                    case "monster":
                        # from quests.hunt import hunt
                        # return hunt(request["target"], request["quantity"])
                        pass
                    case "task":
                        pass
                    case "gather":
                        from quests.gather import gather_quest
                        return gather_quest(request["target"], request["quantity"])
        
        return None  # No suitable quest found

    @staticmethod
    def release_request(quest_type:str, target:str, hero_name:str):
        town_hall.resource_requests = [
            r for r in town_hall.resource_requests
            if not (r["type"] == quest_type and r["target"] == target and r["assigned_to"] == hero_name)
        ]

    @staticmethod
    async def report_need(quest_type:str, target:str, quantity:int, priority: int, requester:str, assigned_to:str):
        for req in town_hall.resource_requests:
            if req["type"] == quest_type and req["target"] == target and req["requester"] == requester:
                req["quantity"] = max(req["quantity"], quantity)
                return
            
        town_hall.resource_requests.append({
            "type":quest_type,
            "target":target,
            "quantity":quantity,
            "priority":priority,
            "requester":requester,
            "assigned_to": None
        })
        town_hall.resource_requests.sort(key=lambda x: x["priority"], reverse=True)

    @staticmethod
    async def create_quest(quest_type:str, details:dict):
        """Factory de quêtes basées sur le type et les détails."""
        pass
    
    @staticmethod
    async def get_stock(item_code):
        if len(town_hall.bank_cache) < 1:
            town_hall.bank_cache = await town_hall.action.bank.get_bank_inventory()
        
        return check_quantity_in_bag(town_hall.bank_cache, item_code)
    
    @staticmethod
    async def define_quest_type(item_code):
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