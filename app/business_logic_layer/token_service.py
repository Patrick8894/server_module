from jose import jwt
from datetime import datetime, timedelta
from .crypto_service import CryptoService
from .base_service import BaseService
from ..common.decorators import singleton
from ..common.logger import token_logger
from ..common.constants import JWT_ALGORITHM, JWT_EXPIRATION, JWT_SECRET, TOKEN_SECRET
from typing import Dict

@singleton
class TokenService(BaseService):
    _logger = token_logger

    def __init__(self, crypto_service: CryptoService):
        self._crypto_service = crypto_service
        
    def create_token(self, payload: Dict) -> str:
        with self.handle_exception():
            exp = datetime.now() + timedelta(seconds=int(JWT_EXPIRATION))
            payload.update({"exp": exp})

            jwt_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

            return self._crypto_service.encrypt_data(jwt_token, TOKEN_SECRET)
    
    def decode_token(self, token: str) -> Dict:
        with self.handle_exception():
            jwt_token = self._crypto_service.decrypt_data(token, TOKEN_SECRET)
            
            return jwt.decode(jwt_token, JWT_SECRET, algorithms=JWT_ALGORITHM)