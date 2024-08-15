from ..common.logger import middleware_logger
from fastapi import HTTPException
from ..common.constants import ENV, TEST_ENV
from ..business_logic_layer.crypto_service import CryptoService
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, crypto_service: CryptoService):
        super().__init__(app)
        self._crypto_service = crypto_service

    async def dispatch(self, request, call_next):
        if (path := request.url.path) in ['docs', 'openapi.json'] or path.startswith("/auth"):
            middleware_logger.info("auth request")
            return await call_next(request)

        if ENV in TEST_ENV:
            middleware_logger.info("auth pass in test env")
            return await call_next(request)
        
        token = request.cookies.get("access_token", "")
        if (user_info := await self._crypto_service.decrypt_token(token)) is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        request.state.user_info = user_info

        return await call_next(request)

        