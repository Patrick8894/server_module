from .base_repository import BaseRepository
from ..common.logger import user_logger
from ..common.decorators import singleton
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime
from typing import Dict

@singleton
class UserRepository(BaseRepository):
    _logger = user_logger

    class CollectionWrapper(BaseRepository.CollectionWrapper):
        pass

    def __init__(self, user_collection: AsyncIOMotorCollection, counter_collection: AsyncIOMotorCollection):
        self._collection = self.CollectionWrapper(user_collection)
        self._counter = counter_collection

    async def create_user(self, name: str, title: str, password: str) -> bool:

        id = await self.get_next_sequence(self._collection._name)
            
        user = {
            "_id": id,
            "name": name,
            "password": password,
            "title": title,
            "post_ids": [],
            "created_timestamp": datetime.now().timestamp(),
            "edited_timestamp": datetime.now().timestamp(),
            "is_deleted": False
        }

        return await self._collection.insert_one(user)
    
    async def get_user(self, _id: str) -> Dict:
            
        return await self._collection.find_one(filter={"_id": _id})
    
    async def get_users(self) -> list:
            
        return await self._collection.find_many(filter={})
    
    async def update_user(self, _id: str, update: Dict) -> bool:

        return await self._collection.update_one(filter={"_id": _id}, update={"$set": update})
    
    async def delete_user(self, _id: str) -> bool:
            
        return await self._collection.delete_one(filter={"_id": _id})