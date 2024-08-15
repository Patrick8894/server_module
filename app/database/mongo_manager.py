from motor.motor_asyncio import AsyncIOMotorClient
from ..common.decorators import singleton
from ..common.constants import DB_NAME, MONGO_HOST, MONGO_PORT
from typing import Literal

@singleton
class AsyncMongoManager:
    COLLECTION = Literal["users", "posts"]
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client[DB_NAME]

    def get_collection(self, collection_name: COLLECTION):
        return self.db[collection_name]

    def close(self):
        self.client.close()

    def drop_collection(self, collection_name: COLLECTION):
        self.db.drop_collection(collection_name)