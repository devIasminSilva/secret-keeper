import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

class CryptoService:
    # Constants
    SALT_SIZE = 32
    NONCE_SIZE = 16
    KEY_SIZE = 32
    TAG_SIZE = 16
    SCRYPT_N = 16384
    SCRYPT_R = 8
    SCRYPT_P = 1

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derives a 32-byte key from the password and salt."""
        return scrypt(password, salt, key_len=CryptoService.KEY_SIZE, N=CryptoService.SCRYPT_N, r=CryptoService.SCRYPT_R, p=CryptoService.SCRYPT_P)

    @staticmethod
    def encrypt_file(input_path: str, password: str, output_path: str = None):
        """
        Encrypts a file using AES-GCM.
        Format: [Salt 32][Nonce 16][Ciphertext][Tag 16]
        """
        if not output_path:
            output_path = input_path + ".enc"

        salt = get_random_bytes(CryptoService.SALT_SIZE)
        key = CryptoService.derive_key(password, salt)
        nonce = get_random_bytes(CryptoService.NONCE_SIZE)
        
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        with open(input_path, 'rb') as f:
            data = f.read() 
        
        ciphertext, tag = cipher.encrypt_and_digest(data)

        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(nonce)
            f.write(ciphertext)
            f.write(tag)
        
        return output_path

    @staticmethod
    def decrypt_file(input_path: str, password: str, output_path: str = None):
        """
        Decrypts a file encrypted with encrypt_file.
        """
        if not output_path:
            output_path = os.path.splitext(input_path)[0]

        with open(input_path, 'rb') as f:
            salt = f.read(CryptoService.SALT_SIZE)
            nonce = f.read(CryptoService.NONCE_SIZE)
            if len(salt) != CryptoService.SALT_SIZE or len(nonce) != CryptoService.NONCE_SIZE:
                raise ValueError("Valid file header not found.")
            
            remaining = f.read()
            if len(remaining) < CryptoService.TAG_SIZE:
                raise ValueError("File is too short to contain valid ciphertext.")
                
            ciphertext = remaining[:-CryptoService.TAG_SIZE]
            tag = remaining[-CryptoService.TAG_SIZE:]

        key = CryptoService.derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            with open(output_path, 'wb') as f:
                f.write(plaintext)
            return output_path
        except ValueError:
            raise ValueError("Decryption failed. Invalid password or corrupted file.")
