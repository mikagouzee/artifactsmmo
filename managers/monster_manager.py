import math
from managers.db_manager import DatabaseManager
from models import hero


async def get_best_monster(my_hero:hero):
    collection = DatabaseManager.get_collection("monsters")

    # Requête MongoDB standard (asynchrone)
    crt_level = my_hero.level
    gt = max(0, crt_level-10)
    query = {
        "level": {"$lte": crt_level, "$gt": gt}
    }

    candidates = await collection.find(query).to_list(length=100)
    if not candidates:
        return None
    
    elements = ["fire", "earth", "water", "air"]
    best_monster = None
    min_turns = float('inf')

    for monster in candidates:
        total_dpt_H = my_hero.dmg
        for e in elements:
            h_atk = getattr(my_hero, f"attack_{e}", 0)
            m_res = monster.get(f'res_{e}', 0)
            total_dpt_H += h_atk * (1 - (m_res/100))

        if total_dpt_H <= 0: continue #ignore this mob, we can't hurt it

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

        if is_survivable and ttk < min_turns:
            min_turns = ttk
            best_monster = monster

    return best_monster.get("code") if best_monster else "chicken"