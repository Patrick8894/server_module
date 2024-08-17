from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs
from .api import startup, auth, user, post
from starlette.middleware.cors import CORSMiddleware
from .api import *
from .api.middleware import AuthMiddleware
from .common.constants import ENV, TEST_ENV
from .business_logic_layer import get_user_service

if ENV in TEST_ENV:
    server = FastAPI(root_path="/api")
    StandaloneDocs(app=server)
    server.docs_url = "/api/docs"
    server.redoc_url = "/api/redoc"
else:
    server = FastAPI(root_path="/api", docs_url=None, redoc_url=None)

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
server.add_middleware(AuthMiddleware, user_service=get_user_service())

server.include_router(startup.router)

server.include_router(auth.router)

server.include_router(user.router)

server.include_router(post.router)

@server.get("")
def read_root():
    return {"Hello World"}

