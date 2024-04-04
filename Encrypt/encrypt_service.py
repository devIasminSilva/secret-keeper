import os
import shutil
import secrets
import struct
from tkinter import messagebox
from Crypto.Cipher import AES

class EncryptService:
    def __init__(self):
        pass

    def encrypt_folder(self, folder_path, password):
        bufferSize = 1024*1024
        key = self.generate_key()

        try:
            zip_filename = folder_path + ".zip"
            shutil.make_archive(folder_path, 'zip', folder_path)

            encrypted_zip_filename = zip_filename + ".enc"
            self.encrypt_file(key, zip_filename, encrypted_zip_filename, bufferSize)

            key_filename = folder_path + ".key"
            self.save_key_to_file(key, key_filename)

            os.remove(zip_filename)

            messagebox.showinfo("Success", "Folder encrypted successfully. Remember to store the encryption key securely.")

        except Exception as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Encryption failed.")

    def generate_key(self):
        return secrets.token_bytes(32)

    def encrypt_file(self, key, in_filename, out_filename, chunksize=64*1024):
        if not out_filename:
            out_filename = in_filename + '.enc'

        iv = os.urandom(16)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    def save_key_to_file(self, key, filename):
        with open(filename, 'wb') as key_file:
            key_file.write(key)