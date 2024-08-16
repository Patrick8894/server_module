from typing import Dict
from ..common.logger import crypto_logger
from .base_service import BaseService

class CryptoService(BaseService):

    _logger = crypto_logger

    def __init__(self):
        pass

    def encrypt(self, data: str) -> str:
        return self.crypto.encrypt(data)

    def decrypt(self, data: str) -> str:
        return self.crypto.decrypt(data)
    
    async def decrypt_token(self, token: str) -> Dict:
        return {"token": token}