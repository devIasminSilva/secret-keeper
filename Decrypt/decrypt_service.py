import os
import struct
from tkinter import messagebox
from Crypto.Cipher import AES

class DecryptService:
    def __init__(self):
        pass

    def decrypt_file(self, file_path, key_path):
        try:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()

            out_filename = os.path.splitext(file_path)[0]

            with open(file_path, 'rb') as infile:
                origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
                iv = infile.read(16)
                decryptor = AES.new(key, AES.MODE_CBC, iv)

                with open(out_filename, 'wb') as outfile:
                    while True:
                        chunk = infile.read(64*1024)
                        if len(chunk) == 0:
                            break
                        outfile.write(decryptor.decrypt(chunk))

                    outfile.truncate(origsize)

            messagebox.showinfo("Success", "File decrypted successfully.")

        except Exception as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Decryption failed.")