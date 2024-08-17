from ..business_logic_layer.crypto_service import CryptoService
from ..business_logic_layer.token_service import TokenService
from ..business_logic_layer.user_service import UserService
from ..data_access_layer.user_repository import UserRepository
import pytest

class TestUserService:

    @pytest.fixture(autouse=True)
    def setup(self, mock_motor_collection):
        self.db = mock_motor_collection
        self.crypto_service = CryptoService()
        self.token_service = TokenService(self.crypto_service)
        self.user_repository = UserRepository(self.db['users'])
        self.service = UserService(self.crypto_service, self.token_service, self.user_repository)