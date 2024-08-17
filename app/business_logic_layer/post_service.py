from .base_service import BaseService
from .user_service import UserService
from ..data_access_layer.post_repository import PostRepository
from ..common.logger import user_logger
from ..common.constants import ACCOUNT_SECRET
from typing import Dict, List

class PostService(BaseService):

    _logger = user_logger

    def __init__(self, user_service: UserService, post_repositoy: PostRepository):
        self._user_service = user_service
        self._post = post_repositoy
    
    async def get_post(self, post_id: str) -> Dict:
        return await self._post.get_post(post_id)
    
    async def get_posts(self) -> List[Dict]:
        return await self._post.get_posts()
    
    async def create_post(self, user_id: str, title: str, description: str) -> bool:

        if not (id := await self._post.generate_id()):
            return False

        return await self._post.create_post(id, title, description, user_id)
    
    async def update_post(self, post_id: str, title: str, description: str) -> bool:
        
        return await self._post.update_post({"_id": post_id}, {"title": title, "description": description})
    
    async def delete_post(self, post_id: str) -> bool:
        
        return await self._post.delete_post(post_id)
        