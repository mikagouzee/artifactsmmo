import math

def can_survive(context, monster) -> bool:
    hero = context.current_hero
    
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
    total_dpt_H = hero.dmg
    for e in elements:
        h_atk = getattr(hero, f"attack_{e}", 0)
        m_res = monster.get(f'res_{e}', 0)
        total_dpt_H += h_atk * (1 - (m_res/100))

    ttk = math.ceil(monster["hp"] / total_dpt_H) 
    
    available_potions = context.get_equiped_healing_potions()

    current_hp = hero.max_hp
    for turn in range(1, ttk + 1):
        # Apply potion logic at start of turn
        if current_hp < (hero.max_hp * 0.5):
            for potion in available_potions:
                if potion["quantity"] > 0:
                    current_hp = min(current_hp + potion["restore"], hero.max_hp)
                    potion["quantity"] -= 1
                    break  # une seule potion par tour

        current_hp -= monster_dpt
        if current_hp <= 0:
            return False
        
    return True