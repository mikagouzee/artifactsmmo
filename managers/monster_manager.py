import math
from managers.db_manager import DatabaseManager
from models import hero


class monster_manager:
    @classmethod
    async def get_best_monster(self, my_hero:hero):
        candidates = await self.get_candidates(self, my_hero)
        
        best_monster = None
        best_ratio = float('-inf')
        xp_expected = float('-inf')
        min_turns = float('-inf')

        for monster in candidates:
            ttk = await self.time_to_kill(self, my_hero, monster)

            if ttk < min_turns:
                min_turns = ttk

            xp_to_gain = self.calculate_xp(self, monster, my_hero.level)
            # print(f"Monster {monster["name"]} should reward {xp_to_gain} xp to {my_hero.name} in {ttk} turns")
            if xp_to_gain//ttk > best_ratio:
                best_monster = monster
                best_ratio = xp_to_gain//ttk
                min_turns = ttk
                xp_expected = xp_to_gain

        result_code = best_monster.get("code") if best_monster else "chicken"
        print(f"{my_hero.name} is going to fight {result_code} : Xp expected {xp_expected}")
        return result_code

    def calculate_xp(self, monster, player_level):
        monster_level = monster["level"]
        monster_hp = monster["hp"]
        level_penalty = self.calculate_level_penalty(self, monster_level, player_level)
        monster_multiplier = 1
        match monster["type"]:
            case "elite":
                monster_multiplier = 1.4
            case "boss":
                monster_multiplier = 2
            
        xp = round(((monster_level / player_level) * 20 + monster_hp * 0.04) * level_penalty * monster_multiplier)
        return xp

    def calculate_level_penalty(self, monster_level, player_level):
        if monster_level >= player_level:
            return 1.0
        elif monster_level - player_level >= 5:
            return 0.7
        elif monster_level - player_level >= 10:
            return 0.0
        else:
            return 1.0 - ((monster_level - player_level) / 10)

    async def get_candidates(self, my_hero:hero):
        collection = DatabaseManager.get_collection("monsters")

        # Requête MongoDB standard (asynchrone)
        crt_level = my_hero.level
        gt = max(0, crt_level-10)
        query = {
            "level": {"$lte": crt_level, "$gt": gt}
        }

        candidates = await collection.find(query).to_list(length=100)
        if not candidates:
            return "chicken"
        return candidates
        
    async def time_to_kill(self, my_hero, monster):
        elements = ["fire", "earth", "water", "air"]
    
        total_dpt_H = my_hero.dmg
        for e in elements:
            h_atk = getattr(my_hero, f"attack_{e}", 0)
            m_res = monster.get(f'res_{e}', 0)
            total_dpt_H += h_atk * (1 - (m_res/100))

        if total_dpt_H <= 0: 
            return 1000 #ignore this mob, we can't hurt it

        total_dpt_M = sum(
                monster.get(f"attack_{e}", 0) * (1 - (getattr(my_hero, f"res_{e}", 0) / 100 ))
                for e in elements
            )
        
        ttk = math.ceil(monster["hp"] / total_dpt_H)
        ttd = math.ceil(my_hero.max_hp / max(total_dpt_M, 0.1) )

        is_survivable = False

        if ttk+3 < ttd:
            is_survivable = True
        elif ttk+3 == ttd and my_hero.initiative > monster.get("initiative", 0):
            is_survivable = True

        if is_survivable:
            return ttk
        else:
            return 1000
