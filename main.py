import asyncio
import os

import httpx
from controllers import ActionController, DbController

from managers.db_manager import DatabaseManager
from workers import farm, farm_combat, farm_craft, farm_task

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
        
        ##INIT DATABASE
        await DatabaseManager.init_db()
        await sync_data(db_controller)

        heroes = await action_controller.get_all_heroes()
        semet = heroes[0]
        ethina = heroes[1]
        kaarl = heroes[2]
        alchie = heroes[3]
        bobby = heroes[4]

        # 3. On dispatch
        tasks = [
            farm_task(semet, action_controller, db_controller).run(),
            farm_task(kaarl, action_controller, db_controller).run(),
            farm_task(ethina, action_controller, db_controller).run(),
            farm_task(bobby, action_controller, db_controller).run(),
            farm_task(alchie, action_controller, db_controller).run()
        ]

        # 4. On lance tout en parallèle
        await asyncio.gather(*tasks)


async def sync_data(db_controller:DbController):
    map_count = await DatabaseManager.db["map_tiles"].count_documents({})
    if map_count == 0:
        await db_controller.sync_world_map()

    res_count = await DatabaseManager.db["resources"].count_documents({})
    if res_count == 0:
        await db_controller.sync_resources()

    monster_count = await DatabaseManager.db["monsters"].count_documents({})
    if monster_count == 0:
        await db_controller.sync_monsters()

    items_count = await DatabaseManager.db["items"].count_documents({})
    if items_count == 0:
        await db_controller.sync_items()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt du bot...")
        