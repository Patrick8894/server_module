from ..business_logic_layer.crypto_service import CryptoService
from ..business_logic_layer.token_service import TokenService
from ..business_logic_layer.user_service import UserService
from ..business_logic_layer.post_service import PostService
from ..data_access_layer.user_repository import UserRepository
from ..data_access_layer.post_repository import PostRepository
import pytest

class TestPostService:

    @pytest.fixture(autouse=True)
    def setup(self, mock_motor_collection):
        self.db = mock_motor_collection
        self.crypto_service = CryptoService()
        self.token_service = TokenService(self.crypto_service)
        self.user_repository = UserRepository(self.db['users'])
        self.user_service = UserService(self.crypto_service, self.token_service, self.user_repository)
        self.post_repository = PostRepository(self.db['posts'])
        self.service = PostService(self.user_service, self.post_repository)