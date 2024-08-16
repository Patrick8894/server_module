from .base_repository import BaseRepository
from ..common.logger import user_logger
from ..common.decorators import singleton
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime
from typing import Dict, List

@singleton
class UserRepository(BaseRepository):
    _logger = user_logger

    class CollectionWrapper(BaseRepository.CollectionWrapper):
        pass

    def __init__(self, user_collection: AsyncIOMotorCollection):
        self._collection = self.CollectionWrapper(user_collection)
        self._collection.create_index([('name', 1)])

    async def create_user(self, user_id: str, user_name: str, title: str, secret: str, password: str, password_salt: str) -> bool:
            
        user = {
            "_id": user_id,
            "name": user_name,
            "password": password,
            "password_salt": password_salt,
            "title": title,
            "post_ids": [],
            "secret": secret,
            "created_timestamp": datetime.now().timestamp(),
            "edited_timestamp": datetime.now().timestamp(),
            "is_deleted": False
        }

        return await self._collection.insert_one(user)
    
    async def get_user(self, _id: str) -> Dict:
            
        return await self._collection.find_one(filter={"_id": _id, "is_deleted": False})
    
    async def get_users(self) -> List:
            
        return await self._collection.find_many(filter={"is_deleted": False})
    
    async def update_user(self, _id: str, update: Dict) -> bool:

        update["edited_timestamp"] = datetime.now().timestamp()

        return await self._collection.update_one(filter={"_id": _id}, update={"$set": update})
    
    async def delete_user(self, _id: str) -> bool:
            
        return await self._collection.update_one(filter={"_id": _id}, update={"$set": {"is_deleted": True}})