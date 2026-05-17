import asyncio
import os
import httpx

from controllers import ActionController, DbController
from controllers.managers import DatabaseManager
from runners import GameRunner


async def main():
    BASE_URL = os.getenv('BASE_URL')
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
        action = ActionController(http_client)
        db = DbController(http_client)
        await DatabaseManager.init_db()
        await db.sync_data()

        runner = GameRunner(action, db)
        await runner.initialize()
        await runner.run()

if __name__ == "__main__":
    asyncio.run(main())