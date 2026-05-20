import math

def can_survive(hero, monster) -> bool:
    # 1. Calcul des dégâts moyens du monstre par tour (en incluant le critique)
    elements = ["fire", "earth", "water", "air"]
    crit_multiplier = 1 + (monster.get("critical_strike", 0) / 100 * 0.5)
    
    # Dégâts totaux du monstre ajustés par la résistance du héros
    monster_dpt = sum(
        monster.get(f"attack_{e}", 0) * (1 - (getattr(hero, f"res_{e}", 0) / 100))
        for e in elements
    ) * crit_multiplier
    
    # Sécurité : éviter la division par zéro
    monster_dpt = max(monster_dpt, 0.1)
    
    # 2. Calcul du temps de survie (TTD) et temps pour tuer (TTK)
    # TTK: calculé comme dans ton code actuel
    total_dpt_H = hero.dmg
    for e in elements:
        h_atk = getattr(hero, f"attack_{e}", 0)
        m_res = monster.get(f'res_{e}', 0)
        total_dpt_H += h_atk * (1 - (m_res/100))
    ttk = math.ceil(monster["hp"] / total_dpt_H) 
    
    # TTD: combien de tours le héros survit
    ttd = math.ceil(hero.max_hp / monster_dpt)
    
    # 3. Condition de survie
    # On ajoute une marge de 3 tours pour compenser les RNG/Miss/Coûts de ticks
    if (ttk + 3) < ttd:
        return True
    elif (ttk + 3) == ttd and hero.initiative > monster.get("initiative", 0):
        return True
        
    return False