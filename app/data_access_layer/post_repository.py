from .base_repository import BaseRepository
from ..common.logger import post_logger
from ..common.decorators import singleton
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime
from typing import Dict, List

@singleton
class PostRepository(BaseRepository):
    _logger = post_logger

    class CollectionWrapper(BaseRepository.CollectionWrapper):
        pass

    def __init__(self, post_collection: AsyncIOMotorCollection):
        self._collection = self.CollectionWrapper(post_collection)
        self._collection.create_index([('title', 1)])

    async def create_post(self, _id: str, title: str, description: str, user_id: str) -> bool:
            
        post = {
            "_id": _id,
            "title": title,
            "description": description,
            "user_id": user_id,
            "created_timestamp": datetime.now().timestamp(),
            "edited_timestamp": datetime.now().timestamp(),
            "is_deleted": False
        }

        return await self._collection.insert_one(post)
    
    async def get_post(self, _id: str) -> Dict:
            
        if (post := await self._collection.aggregate(
            [
                {"$match": {"_id": _id, "is_deleted": False}},
                {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
                {"$unwind": "$user"},
                {"$project": {"_id": 0, "post_id": "$_id", "title": 1, "description": 1, "user_id": 1, "user_name": "$user.name", "created_timestamp": 1, "edited_timestamp": 1}}
            ]
        )): return post[0]
    
    async def get_posts(self) -> List:
            
        return await self._collection.aggregate(
            [
                {"$match": {"is_deleted": False}},
                {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
                {"$unwind": "$user"},
                {"$project": {"_id": 0, "post_id": "$_id", "title": 1, "description": 1, "user_id": 1, "user_name": "$user.name", "created_timestamp": 1, "edited_timestamp": 1}}
            ]
        )
    
    async def update_post(self, _id: str, update: Dict) -> bool:

        update["edited_timestamp"] = datetime.now().timestamp()

        return await self._collection.update_one(filter={"_id": _id}, update={"$set": update})
    
    async def delete_post(self, _id: str) -> bool:
            
        return await self._collection.update_one(filter={"_id": _id}, update={"$set": {"is_deleted": True}})
    
    async def generate_id(self) -> str:

        return await self._collection.generate_id()