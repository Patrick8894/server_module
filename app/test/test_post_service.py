from ..business_logic_layer.crypto_service import CryptoService
from ..business_logic_layer.token_service import TokenService
from ..business_logic_layer.user_service import UserService
from ..business_logic_layer.post_service import PostService
from ..data_access_layer.user_repository import UserRepository
from ..data_access_layer.post_repository import PostRepository
import pytest
import pytest_asyncio
from . import mock_motor_collection
from typing import Dict

class TestPostService:

    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, mock_motor_collection: Dict):
        self.db = mock_motor_collection
        self.crypto_service = CryptoService()
        self.token_service = TokenService(self.crypto_service)
        self.user_repository = UserRepository(self.db['users'])
        self.user_service = UserService(self.crypto_service, self.token_service, self.user_repository)
        self.post_repository = PostRepository(self.db['posts'])
        self.service = PostService(self.user_service, self.post_repository)
        await self.user_repository._collection._collection.delete_many({})
        await self.post_repository._collection._collection.delete_many({})

    @pytest.mark.asyncio
    async def test_post_crud(self):
        assert await self.user_service.create_user("user_id", "test_name", "test_title", "test_secret", "test_password")
        assert (id := await self.service.create_post("user_id", "test_title", "test_description"))
        assert await self.service.get_post(id) is not None

        assert (id2 := await self.service.create_post("user_id", "test_title2", "test_description2"))
        assert await self.service.get_post(id2) is not None

        assert await self.service.get_posts() is not None

        assert await self.service.update_post(id, "test_title3", "test_description3")
        assert (post := await self.service.get_post(id))
        assert post['title'] == "test_title3"
        assert post['description'] == "test_description3"

        assert await self.service.delete_post(id)
        assert not await self.service.get_post(id)