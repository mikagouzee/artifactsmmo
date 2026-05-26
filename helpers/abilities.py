
from helpers.combat import can_survive

async def can_fulfill(context, request, db) -> bool:  
    target = request["target"]
    hero = context.current_hero
    quest_type = request["type"]

    match quest_type:
        case "craft":
            db_item = await db.item.find_by_code(target)
            if not db_item:
                return False

            required_profession = db_item.get("craft", {}).get("skill") # ex: "mining"
            required_level = db_item.get("craft", {}).get("level")     # ex: 10    
            skill_name = f"{required_profession}_level"
            hero_level = getattr(hero, skill_name)
            return hero_level >= required_level 

        case "gather":
            db_item = await db.item.find_by_code(target)
            if not db_item:
                return False
            required_profession = db_item.get("subtype", "")
            required_level = db_item.get("level", 1)
            skill_name = f"{required_profession}_level"
            hero_level = getattr(hero, skill_name)
            return hero_level >= required_level
        
        case "task_buy":
            #should be a check on global task accomplished but ¯\_(ツ)_/¯
            return False
        
        case "monster":
            target_monster = await db.monsters.find_by_code(target)
            return can_survive(context, target_monster)

        case _:
            return False