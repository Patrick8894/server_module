from .base_service import BaseService
from .crypto_service import CryptoService
from .token_service import TokenService
from ..data_access_layer.user_repository import UserRepository
from ..common.logger import user_logger
from ..common.constants import ACCOUNT_SECRET
from typing import Dict, List

class UserService(BaseService):
    _logger = user_logger

    def __init__(self, crypto_service: CryptoService, token_service: TokenService, user_repositoy: UserRepository):
        self._crypto_service = crypto_service
        self._token_service = token_service
        self._user = user_repositoy

    def generate_user_token(self, user_info: Dict) -> str:
        return self._token_service.create_token(user_info)
    
    async def decode_user_token(self, token: str) -> Dict:
        return self._token_service.decode_token(token)
    
    async def user_login(self, user_id: str, password: str) -> str:
        if not (user_info := await self._user.get_user(user_id)):
            return None
        
        password_hash = self._crypto_service.hash_password(password, user_info["password_salt"])

        if password_hash != user_info["password"]:
            return None
        
        return {"user_id": user_info['_id']}
    
    async def get_user(self, user_id: str) -> Dict:
        if (user_info := await self._user.get_user(user_id)):
            user_info['secret'] = self._crypto_service.decrypt_data(user_info['secret'], ACCOUNT_SECRET)

        return user_info
    
    async def get_users(self) -> List[Dict]:
        if (user_infos := await self._user.get_users()) is None:
            return None

        return user_infos
    
    async def create_user(self, user_id: str, user_name: str, title: str, secret: str, password: str) -> bool:
        
        password_salt = self._crypto_service.generate_salt()
        password_hash = self._crypto_service.hash_password(password, password_salt)

        encrypted_secret = self._crypto_service.encrypt_data(secret, ACCOUNT_SECRET)

        return await self._user.create_user(user_id, user_name, title, encrypted_secret, password_hash, password_salt)
    
    async def update_user(self, user_id: str, user_name: str, title: str, secret: str, password: str) -> bool:

        password_salt = self._crypto_service.generate_salt()
        password_hash = self._crypto_service.hash_password(password, password_salt)

        encrypted_secret = self._crypto_service.encrypt_data(secret, ACCOUNT_SECRET)
        
        return await self._user.update_user(user_id, {"name": user_name, "title": title, "secret": encrypted_secret, "password": password_hash, "password_salt": password_salt})
    
    async def delete_user(self, user_id: str) -> bool:
        
        return await self._user.delete_user(user_id)
        