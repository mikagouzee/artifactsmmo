import math

def time_to_kill(my_hero, monster):
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