from helpers import can_survive


async def can_fulfill(context, request, db) -> bool:
    
    item_code = request["item_code"]
    hero = context.current_hero

    # 1. Aller chercher les infos de l'item dans ta DB Mongo statique
    db_item = await db.item.find_by_code(item_code)
    if not db_item:
        return False
    
    match request["type"]:
        case "craft":
            required_profession = db_item.get("craft", {}).get("skill") # ex: "mining"
            required_level = db_item.get("craft", {}).get("level")     # ex: 10    
            skill_name = f"{required_profession}_level"
            hero_level = getattr(hero, skill_name)
            return hero_level >= required_level 

        case "gather":
            required_profession = db_item.get("subtype", "")
            required_level = db_item.get("level", 1)
            skill_name = f"{required_profession}_level"
            hero_level = getattr(hero, skill_name)
            return hero_level >= required_level
        
        case "task_buy":
            #should be a check on global task accomplished but ¯\_(ツ)_/¯
            return False
        
        case "monster":
            target_monster = db.monsters.find_by_loot(item_code)
            return can_survive(context, target_monster)

        case _:
            return False