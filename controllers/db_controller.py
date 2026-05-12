# db_controller.py
from managers.db_manager import DatabaseManager

class DbController:
    def __init__(self, http_client):
        self.http = http_client

    async def sync_resources(self):
        collection = DatabaseManager.db["resources"]
        
        response = await self.http.get("/resources")
        resources = response.json().get("data", [])

        for res in resources:
            await collection.replace_one(
                {"code": res["code"]},
                res,
                upsert=True
            )
        print(f"Synced {len(resources)} resources.")

    async def sync_world_map(self):
        collection = DatabaseManager.db["map_tiles"]
        page = 1
        
        while True:
            response = await self.http.get("/maps", params={"page": page, "size": 100})
            data = response.json()
            maps_data = data.get("data", [])

            for tile in maps_data:
                await collection.replace_one(
                    {"x": tile["x"], "y": tile["y"]}, # Clé unique par coordonnées
                    tile,
                    upsert=True
                )

            if page >= data.get("pages", 1):
                break
            page += 1
        print("Synced WorldMap.")