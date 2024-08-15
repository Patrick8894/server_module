from logging import Logger
from motor.motor_asyncio import AsyncIOMotorCollection
from ..common.decorators import suppress_exceptions
from typing import Dict, Optional, List

class BaseRepository:
    _logger: Logger
    _counter: AsyncIOMotorCollection

    class CollectionWrapper():
        def __init__(self, collection: AsyncIOMotorCollection):
            self._collection = collection
            self._name = collection.name

        def __getattribute__(self, name: str):
            attr = object.__getattribute__(self, name)
            if callable(attr) and not name.startswith("_"):
                def wrapper(*args, **kwargs):
                    return suppress_exceptions(attr)(*args, **kwargs)
                return wrapper
            return attr
        
        async def find_one(self, filter: Dict, projection: Optional[Dict] = None) -> Dict:

            if (result := await self._collection.find_one(filter=filter, projection=projection)) is None:
                return {}

            return result
        
        async def find_many(self, filter: Dict, projection: Optional[Dict] = None) -> List[Dict]:

            return [doc async for doc in self._collection.find(filter=filter, projection=projection)]
        
        async def insert_one(self, data: Dict) -> bool:

            result = await self._collection.insert_one(data)
            return result.acknowledged
        
        async def insert_many(self, data: List[Dict]) -> bool:

            result = await self._collection.insert_many(data)
            return result.acknowledged
        
        async def update_one(self, filter: Dict, update: Dict, upsert: Optional[bool] = True) -> bool:
                
            result = await self._collection.update_one(filter=filter, update=update, upsert=upsert)
            return result.acknowledged
        
        async def update_many(self, filter: Dict, update: Dict, upsert: Optional[bool] = True) -> bool:
                
            result = await self._collection.update_many(filter=filter, update=update, upsert=upsert)
            return result.acknowledged
        
        async def delete_one(self, filter: Dict) -> bool:

            result = await self._collection.delete_one(filter=filter)
            return result.acknowledged
        
        async def delete_many(self, filter: Dict) -> bool:

            result = await self._collection.delete_many(filter=filter)
            return result.acknowledged
        
        async def replace_one(self, filter: Dict, replacement: Dict) -> bool:

            result = await self._collection.replace_one(filter=filter, replacement=replacement)
            return result.acknowledged
        
        async def find_one_and_update(self, filter: Dict, update: Dict, return_document: Optional[bool] = True, upsert: Optional[bool] = True) -> Dict:

            return await self._collection.find_one_and_update(filter=filter, update=update, return_document=return_document, upsert=upsert)
        
        async def aggregate(self, pipeline: List[Dict]) -> List[Dict]:

            return await self._collection.aggregate(pipeline).to_list(None)
        
    async def get_next_sequence(self, sequence_name: str) -> int:

        counter = await self._counter.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"seq": 1}},
            return_document=True,
            upsert=True,
        )

        return counter["seq"]
