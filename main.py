import asyncio
import os

import httpx
from controllers import ActionController, DbController

from managers.db_manager import DatabaseManager
from models.beanies import MapTile, Resource, ResourceDrop
from workers import farm_alchemy, farm_combat, farm_copper, farm_mining, farm_sheeps



async def main():
    BASE_URL = "https://api.artifactsmmo.com"
    DEFAULT_TIME_OUT = 10.0
    HEADERS = {
        "Authorization": f"Bearer {os.getenv('Token')}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }   

    async with httpx.AsyncClient(
        headers=HEADERS,
        base_url = BASE_URL,
        timeout=DEFAULT_TIME_OUT) as http_client:
        action_controller = ActionController(http_client)
        db_controller = DbController(http_client)
        
        ##INIT DATABASE FOR MAPS
        await DatabaseManager.init_db()
        mapcount = await MapTile.count()
        if mapcount == 0:
            db_controller.sync_world_map()
        resource_count = await Resource.count()
        if resource_count == 0:
          await db_controller.sync_resources()
        
        # await action_controller.load_world_map()

        heroes = await action_controller.get_all_heroes()
        semet = heroes[0]
        ethina = heroes[1]
        kaarl = heroes[2]
        alchie = heroes[3]
        bobby = heroes[4]

        # 3. On dispatch
        tasks = [
            farm_mining(semet, action_controller).run(),
            farm_mining(kaarl, action_controller).run(),
            farm_sheeps(ethina, action_controller).run(),
            farm_combat(bobby, action_controller).run(),
            farm_combat(alchie, action_controller).run()
        ]

        # 4. On lance tout en parallèle
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt du bot...")
        