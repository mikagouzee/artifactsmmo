from managers.db_manager import DatabaseManager


async def get_best_resource(current_level:int, skill:str):
    collection = DatabaseManager.get_collection("resources")

    # Requête MongoDB standard (asynchrone)
    gt = current_level-10
    query = {
        "skill": skill,
        "level": {"$lte": current_level, "$gt": gt}
    }

    # On trie par niveau descendant et on prend le premier
    cursor = collection.find(query).sort("level", -1).limit(1)
    results = await cursor.to_list(length=1)

    if not results:
        # Fallback niveau 1
        cursor = collection.find({"skill": skill}).sort("level", 1).limit(1)
        results = await cursor.to_list(length=1)

    return results[0].get("code")