from .db_manager import DatabaseManager

class resource_manager:
    def __init__(self):
        self.collection = []

    def initialize(self):
        self.collection = DatabaseManager.get_collection("resources")

    async def get_best_resource(self, current_level:int, skill:str):
        # Requête MongoDB standard (asynchrone)
        gt = current_level-10
        query = {
            "skill": skill,
            "level": {"$lte": current_level, "$gt": gt}
        }

        # On trie par niveau descendant et on prend le premier
        cursor = self.collection.find(query).sort("level", -1).limit(1)
        results = await cursor.to_list(length=1)

        if not results:
            # Fallback niveau 1
            cursor = self.collection.find({"skill": skill}).sort("level", 1).limit(1)
            results = await cursor.to_list(length=1)

        return results[0].get("code")

    async def get_resource_by_drop(self, drop_code:str):
        query = {
            "drops.code": drop_code
        }
        cursor = self.collection.find(query).limit(1)
        results = await cursor.to_list(length=1)

        return results[0]