import os
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from dotenv import load_dotenv
from models.beanies import MapTile, Resource

load_dotenv()

class DatabaseManager:
    _client: AsyncMongoClient = None
    db = None

    @classmethod
    async def init_db(cls):
        user = os.getenv("MONGO_USER")
        password = os.getenv("MONGO_PASSWORD")
        host = os.getenv("MONGO_HOST", "localhost")
        port = os.getenv("MONGO_PORT", "27017")
        db_name = os.getenv("MONGO_DB_NAME", "artifacts_mmo")

        uri = f"mongodb://{user}:{password}@{host}:{port}"
        cls._client = AsyncMongoClient(uri)

        cls.db = cls._client.get_database(db_name)

        try:
            await cls._client.admin.command('ping')
            print("Connected to mongo!")
        except Exception as e:
            print(f'Error in connection : {e}')        


    @classmethod
    async def close_db(cls):
        if cls._client:
            cls._client.close()