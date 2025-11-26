from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

class AsyncDatabase:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_db(self):
        self.client = AsyncIOMotorClient(settings.MONGO_DB_URL,
                                         uuidRepresentation='standard')
        self.db = self.client[settings.MONGO_DB_NAME]
        print("Connected to MongoDB Atlas...")

    async def close_db_connection(self):
        self.client.close()
        print("Closed MongoDB connection.")

db = AsyncDatabase()