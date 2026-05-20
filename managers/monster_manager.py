import math

from helpers import time_to_kill
from .db_manager import DatabaseManager
from models import hero


class monster_manager:
    def __init__(self):
        self.collection = []
        self.cache = {}

    def initialize(self):
        self.collection = DatabaseManager.get_collection("monsters")

    async def get_best_monster(self, my_hero:hero):
        candidates = await self.get_candidates(my_hero)
        
        best_monster = None
        best_ratio = float('-inf')
        xp_expected = float('-inf')
        min_turns = float('-inf')

        for monster in candidates:
            ttk = time_to_kill(my_hero, monster)

            if ttk < min_turns:
                min_turns = ttk

            xp_to_gain = self.calculate_xp(monster, my_hero.level)
            # print(f"Monster {monster["name"]} should reward {xp_to_gain} xp to {my_hero.name} in {ttk} turns")
            if xp_to_gain//ttk > best_ratio:
                best_monster = monster
                best_ratio = xp_to_gain//ttk
                min_turns = ttk
                xp_expected = xp_to_gain

        result_code = best_monster.get("code") if best_monster else "chicken"
        # print(f"{my_hero.name} is going to fight {result_code} : Xp expected {xp_expected}")
        return result_code

    def calculate_level_penalty(self, monster_level, player_level):
        if monster_level >= player_level:
            return 1.0
        elif monster_level - player_level >= 5:
            return 0.7
        elif monster_level - player_level >= 10:
            return 0.0
        else:
            return 1.0 - ((monster_level - player_level) / 10)


    def calculate_xp(self, monster, player_level):
        monster_level = monster["level"]
        monster_hp = monster["hp"]
        level_penalty = self.calculate_level_penalty(monster_level, player_level)
        monster_multiplier = 1
        match monster["type"]:
            case "elite":
                monster_multiplier = 1.4
            case "boss":
                monster_multiplier = 2
            
        xp = round(((monster_level / player_level) * 20 + monster_hp * 0.04) * level_penalty * monster_multiplier)
        return xp


    async def get_candidates(self, my_hero:hero):
        # Requête MongoDB standard (asynchrone)
        crt_level = my_hero.level
        gt = max(0, crt_level-10)
        query = {
            "level": {"$lte": crt_level, "$gt": gt}
        }

        candidates = await self.collection.find(query).to_list(length=100)
        if not candidates:
            return "chicken"
        return candidates
        
    async def find_by_loot(self, item_code):
        if item_code not in self.cache:
            query= {"drops.code": item_code}        
            queried = await self.collection.find(query).to_list(lenght=1)
            self.cache[item_code]=queried
        return self.cache[item_code]