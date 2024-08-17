from ..database.mongo_manager import AsyncMongoManager
from .user_repository import UserRepository
from .post_repository import PostRepository

def get_user_repository(*collections):
    if not collections:
        collections =  [AsyncMongoManager().get_collection("users")]
    return UserRepository(*collections)

def get_post_repository(*collections):
    if not collections:
        collections =  [AsyncMongoManager().get_collection("posts")]
    return PostRepository(*collections)