
import math

from helpers.craft import check_quantity_in_bag


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

def calculate_level_penalty(monster_level, player_level):
    if monster_level >= player_level:
        return 1.0
    level_diff = player_level - monster_level  # positive when monster is weaker
    if level_diff >= 10:
        return 0.0
    elif level_diff >= 5:
        return 0.7
    else:
        return 1.0 - (level_diff / 10)

def calculate_xp(monster, player_level):
        monster_level = monster["level"]
        monster_hp = monster["hp"]
        level_penalty = calculate_level_penalty(monster_level, player_level)
        monster_multiplier = 1
        match monster["type"]:
            case "elite":
                monster_multiplier = 1.4
            case "boss":
                monster_multiplier = 2
            
        xp = round(((monster_level / player_level) * 20 + monster_hp * 0.04) * level_penalty * monster_multiplier)
        return xp

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
      
      # ttk = math.ceil(monster["hp"] / total_dpt_H)
      # ttd = math.ceil(my_hero.max_hp / max(total_dpt_M, 0.1) )
      ttk = monster["hp"] / total_dpt_H
      ttd = my_hero.max_hp / max(total_dpt_M, 0.1)

      is_survivable = False

      if ttk+3 < ttd:
          is_survivable = True
      elif ttk+3 == ttd and my_hero.initiative > monster.get("initiative", 0):
          is_survivable = True

      if is_survivable:
          return ttk
      else:
          return 1000

def find_best_monster(context, candidates):
        my_hero = context.current_hero
        # candidates = await self.get_candidates(my_hero)

        best_monster = None
        best_ratio = float('-inf')

        for monster in candidates:
            # Hard filter: skip any monster the hero cannot survive
            if not can_survive(context, monster):
                continue

            ttk = time_to_kill(my_hero, monster)
            if ttk >= 1000:
                # time_to_kill signals an unwinnable fight (can't deal damage)
                continue

            xp_to_gain = calculate_xp(monster, my_hero.level)
            ratio = xp_to_gain / ttk
            if ratio > best_ratio:
                best_monster = monster
                best_ratio = ratio

        result_code = best_monster.get("code") if best_monster else "chicken"
        return result_code

def find_best_potion_in_stock(context, bag, healing_potions):
  available = []
  
  if isinstance(bag, dict):
    bag = [{"code":k, "quantity": v} for k, v in bag.items()]

  for item in bag:
    if item["code"] in healing_potions:
      available.append({
        "code":item["code"],
        "value":healing_potions[item["code"]]
      })

  for item in context.current_hero.inventory:
    if item["code"] in healing_potions:
      available.append({
        "code":item["code"],
        "value":healing_potions[item["code"]]
      })

  if not available:
    return None
  
  target_hp = context.current_hero.max_hp
  target_potion = min(available, key=lambda x: abs(x["value"] - target_hp))
  
  return target_potion

async def heal(context, action, db):
  if context.current_hero.hp < context.current_hero.max_hp:
    foods = [item for item in context.current_hero.inventory if item["code"] in db.item.food]
    if foods:
      best_food = max(foods, key=lambda x: db.item.food[x["code"]])
      as_item = await db.item.find_by_code(best_food["code"])
      qtty_to_consume = (context.current_hero.max_hp - context.current_hero.hp) // as_item["effects"][0]["value"] 
      if qtty_to_consume > 0:
        qtty_in_bag = check_quantity_in_bag(context.current_hero.inventory, best_food["code"])
        qtty = min(qtty_in_bag, qtty_to_consume)
        context = await action.hero.use_item(context, best_food["code"], qtty=qtty)
        context = await heal(context, action, db)
      else:
        return context
    elif context.current_hero.hp <= context.current_hero.max_hp /2:
      context = await action.hero.rest(context)
  return context

