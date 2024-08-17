from ..business_logic_layer.crypto_service import CryptoService
import pytest
import os

class TestCryptoService:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = CryptoService()

    def test_encrypt_data(self):
        data = "data"
        key = os.urandom(16).hex()
        encrypted_data = self.service.encrypt_data(data, key)
        assert data != encrypted_data

    def test_decrypt_data(self):
        data = "data"
        key = os.urandom(16).hex()
        encrypted_data = self.service.encrypt_data(data, key)
        decrypted_data = self.service.decrypt_data(encrypted_data, key)
        assert data == decrypted_data

    def test_generate_salt(self):
        salt = self.service.generate_salt()
        assert len(salt) == 32

    def test_hash_password(self):
        password = "password"
        salt = self.service.generate_salt()
        password_hash = self.service.hash_password(password, salt)
        assert len(password_hash) == 64