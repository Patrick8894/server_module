from .crypto_service import CryptoService
from .token_service import TokenService
from .user_service import UserService
from .post_service import PostService
from ..data_access_layer import *

def get_crypto_service():
    return CryptoService()

def get_token_service(*dependencies):
    if not dependencies:
        dependencies = [get_crypto_service()]
    return TokenService(*dependencies)

def get_user_service(*dependencies):
    if not dependencies:
        dependencies = [get_crypto_service(), get_token_service(), get_user_repository()]
    return UserService(*dependencies)

def get_post_service(*dependencies):
    if not dependencies:
        dependencies = [get_user_service(), get_post_repository()]
    return PostService(*dependencies)