import pytest
import os
from core.crypto import CryptoService

def test_crypto_roundtrip(tmp_path):
    input_file = tmp_path / "secret.txt"
    input_file.write_text("This is a secret message.", encoding='utf-8')
    password = "MyStrongPassword123"
    
    encrypted_file = CryptoService.encrypt_file(str(input_file), password)
    assert os.path.exists(encrypted_file)
    assert encrypted_file != str(input_file)
    
    decrypted_file_path = tmp_path / "secret_decrypted.txt"
    CryptoService.decrypt_file(encrypted_file, password, str(decrypted_file_path))
    
    assert os.path.exists(decrypted_file_path)
    assert open(decrypted_file_path, "r", encoding='utf-8').read() == "This is a secret message."

def test_crypto_wrong_password(tmp_path):
    input_file = tmp_path / "secret.txt"
    input_file.write_text("This is a secret message.", encoding='utf-8')
    password = "MyStrongPassword123"
    wrong_password = "WrongPassword"
    
    encrypted_file = CryptoService.encrypt_file(str(input_file), password)
    
    with pytest.raises(ValueError, match="Decryption failed"):
        CryptoService.decrypt_file(encrypted_file, wrong_password)
