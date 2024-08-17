from .base_service import BaseService
from ..common.logger import crypto_logger
from ..common.decorators import singleton
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import hashlib

@singleton
class CryptoService(BaseService):
    _logger = crypto_logger

    def __init__(self):
        pass
    
    def encrypt_data(self, data: str, key: str) -> str:
        data = data.encode()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return (iv + ct).hex()

    def decrypt_data(self, iv_and_ct: str, key: str) -> str:
        iv_and_ct_b64 = bytes.fromhex(iv_and_ct)
        iv = iv_and_ct_b64[:16]
        ct = iv_and_ct_b64[16:]
        cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(ct) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()  # 128-bit block size for AES
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        return decrypted_data.decode()
    
    def generate_salt(self) -> str:
        return os.urandom(16).hex()
    
    def hash_password(self, password: str, salt: str) -> str:
        byte_salt = bytes.fromhex(salt)
        salted_password = byte_salt + password.encode() + byte_salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        return hashed_password