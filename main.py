import asyncio
import os

import httpx
from controllers.action_controller import ActionController
from workers import farm_alchemy, farm_iron, farm_combat, farm_copper, farm_mining, farm_wood



async def main():
    headers = {
        "Authorization": f"Bearer {os.getenv('Token')}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(
        headers=headers,
        base_url = "https://api.artifactsmmo.com",
        timeout=10.0) as http_client:
        controller = ActionController(http_client)
        await controller.load_world_map()

        heroes = await controller.get_all_heroes()
        semet = heroes[0]
        ethina = heroes[1]
        kaarl = heroes[2]
        alchie = heroes[3]
        bobby = heroes[4]

        # 3. On dispatch
        tasks = [
            farm_combat(semet, controller).run(),
            farm_mining(kaarl, controller).run(),
            farm_combat(ethina, controller).run(),
            farm_alchemy(bobby, controller).run(),
            farm_combat(alchie, controller).run()
        ]

        # 4. On lance tout en parallèle
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt du bot...")