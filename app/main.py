from fastapi import FastAPI, APIRouter
from fastapi_standalone_docs import StandaloneDocs
from .common.constants import ENV, TEST_ENV
from .api import startup
from starlette.middleware.cors import CORSMiddleware
from .api import *
from .api.middleware import AuthMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = FastAPI(root_path="/api")
# StandaloneDocs(app=server)

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
server.add_middleware(AuthMiddleware, crypto_service=get_crypto_service())

server.include_router(startup.router)

@server.get("/")
def read_root():
    return {"Hello World"}

