from managers import DatabaseManager
# from helpers import can_survive

class monster_manager:
    def __init__(self):
        self.collection = []
        self.cache = {}
    def initialize(self):
        self.collection = DatabaseManager.get_collection("monsters")

    async def get_candidates(self, context):
        my_hero = context.current_hero
        gt = max(0, my_hero.level-10)
        lte = my_hero.level + 10
        query = {
            "level": {
                "$gt": gt,
                "$lte": lte
                    }
        }

        candidates = await self.collection.find(query).to_list(length=100)
        if not candidates:
            return []
        return candidates
        
    async def find_by_loot(self, item_code):
        if item_code not in self.cache:
            query= {"drops.code": item_code}        
            queried = await self.collection.find(query).to_list(length=1)
            self.cache[item_code]=queried
        return self.cache[item_code]
    
    async def find_by_code(self, monster_code):
        queried = await self.collection.find({'code':monster_code}).to_list(length=1)
        if queried:
            return queried[0]
        else:
            print(f"Monster {monster_code} not found.")
            return None
        
   