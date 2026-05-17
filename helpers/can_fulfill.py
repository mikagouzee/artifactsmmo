async def can_fulfill(hero, request, db) -> bool:
    
    item_code = request["item"]
    
    # 1. Aller chercher les infos de l'item dans ta DB Mongo statique
    item_info = await db.items.find_one({"code": item_code})
    if not item_info:
        return False
        
    # Exemple si c'est une ressource à récolter (mineur, botaniste, etc.)
    required_profession = item_info.get("gathertask", {}).get("code") # ex: "mining"
    required_level = item_info.get("gathertask", {}).get("level")     # ex: 10
    
    if required_profession and required_level:
        # Vérifier le niveau actuel du héros dans ce métier
        skill_name = f"{required_profession}_level"
        hero_level = hero.professions.get(skill_name, 0)
        return hero_level >= required_level

    return False