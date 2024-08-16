from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from ..common.decorators import singleton
from ..common.constants import DB_NAME, MONGO_HOST, MONGO_PORT
from typing import Literal
import asyncio

@singleton
class AsyncMongoManager:
    COLLECTION = Literal["users", "posts"]
    def __init__(self):
        self._client = AsyncIOMotorClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}')
        self._db = self._client[DB_NAME]

    def get_collection(self, collection_name: COLLECTION) -> AsyncIOMotorCollection:
        return self._db[collection_name]

    def close(self):
        self._client.close()

    def drop_collection(self, collection_name: COLLECTION):
        self._db.drop_collection(collection_name)