from ..business_logic_layer.token_service import TokenService
from ..business_logic_layer.crypto_service import CryptoService
import pytest
import os

class TestTokenService:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.crypto_service = CryptoService()
        self.service = TokenService(self.crypto_service)

    def test_create_token(self):
        data = {"data": "data"}
        token = self.service.create_token(data)
        assert token is not None

    def test_decode_token(self):
        data = {"data": "data"}
        token = self.service.create_token(data)
        decoded_data = self.service.decode_token(token)
        assert data == decoded_data