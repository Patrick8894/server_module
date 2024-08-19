from ..business_logic_layer.crypto_service import CryptoService
from ..business_logic_layer.token_service import TokenService
from ..business_logic_layer.user_service import UserService
from ..data_access_layer.user_repository import UserRepository
import pytest
import pytest_asyncio
from . import mock_motor_collection
from typing import Dict

class TestUserService:

    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, mock_motor_collection: Dict):
        self.db = mock_motor_collection
        self.crypto_service = CryptoService()
        self.token_service = TokenService(self.crypto_service)
        self.user_repository = UserRepository(self.db['users'])
        self.service = UserService(self.crypto_service, self.token_service, self.user_repository)
        await self.user_repository._collection._collection.delete_many({})

    @pytest.mark.asyncio
    async def test_register_and_login(self):
        assert await self.service.create_user("test_user", "test_name", "test_title", "test_secret", "test_password")
        assert await self.service.get_user("test_user")

        assert (user_info := await self.service.user_login("test_user", "test_password"))
        assert user_info['user_id'] == "test_user"

        assert (token := self.service.generate_user_token(user_info))
        assert await self.service.decode_user_token(token) == user_info

    @pytest.mark.asyncio
    async def test_user_crud(self):
        assert await self.service.create_user("test_user", "test_name", "test_title", "test_secret", "test_password")
        assert await self.service.get_user("test_user")

        assert await self.service.create_user("test_user2", "test_name2", "test_title2", "test_secret2", "test_password2")
        assert await self.service.get_user("test_user2")

        assert await self.service.get_users()

        assert await self.service.update_user("test_user", "test_name3", "test_title3", "test_secret3", "test_password3")
        assert (user_info := await self.service.get_user("test_user"))
        assert user_info['name'] == "test_name3"
        assert user_info['title'] == "test_title3"
        assert user_info['secret'] == "test_secret3"
        assert await self.service.user_login("test_user", "test_password3") is not None

        assert await self.service.delete_user("test_user")
        assert not await self.service.get_user("test_user")