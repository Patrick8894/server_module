from ..common.logger import middleware_logger
from ..common.constants import ENV, TEST_ENV
from ..business_logic_layer.user_service import UserService
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, user_service: UserService):
        super().__init__(app)
        self._user_service = user_service

    async def dispatch(self, request, call_next):

        if (path := request.url.path) == '/api/openapi.json' or path.startswith("/api/auth") or path.startswith("/api/docs") or path.startswith("/api/redoc"):
            middleware_logger.info("auth request")
            return await call_next(request)

        # if ENV in TEST_ENV:
        #     middleware_logger.info("auth pass in test env")
        #     return await call_next(request)
        
        if not (token := request.cookies.get("access_token")):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        if (user_info := await self._user_service.decode_user_token(token)) is None:
            return JSONResponse(status_code=500, content={"detail": "Failed to decrypt token"})
        
        if not (await self._user_service.get_user(user_info['user_id'])):
            return JSONResponse(status_code=404, content={"detail": "User is already deleted"})

        request.state.user_info = user_info

        return await call_next(request)

        