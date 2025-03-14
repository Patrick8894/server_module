from .base_service import BaseService
from .user_service import UserService
from ..data_access_layer.post_repository import PostRepository
from ..common.logger import post_logger
from ..common.decorators import singleton
from typing import Dict, List

@singleton
class PostService(BaseService):

    _logger = post_logger

    def __init__(self, user_service: UserService, post_repositoy: PostRepository):
        self._user_service = user_service
        self._post = post_repositoy
    
    async def get_post(self, post_id: str) -> Dict:
        return await self._post.get_post(post_id)
    
    async def get_posts(self) -> List[Dict]:
        return await self._post.get_posts()
    
    async def create_post(self, user_id: str, title: str, description: str) -> str:

        if not (id := await self._post.generate_id()):
            return False

        if not await self._post.create_post(id, title, description, user_id):
            return False
        
        return id
    
    async def update_post(self, post_id: str, title: str, description: str) -> bool:
        
        return await self._post.update_post(post_id, {"title": title, "description": description})
    
    async def delete_post(self, post_id: str) -> bool:
        
        return await self._post.delete_post(post_id)
        