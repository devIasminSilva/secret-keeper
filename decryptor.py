import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct
from Crypto.Cipher import AES

class DecryptFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root)

        self.app_manager = app_manager

        self.file_path = tk.StringVar()
        self.key_path = tk.StringVar()

        # Voltar ao menu principal
        back = tk.Button(self, text="Back", command=self.show_menu_frame).pack(side=tk.LEFT)

        # Selecionar arquivo
        tk.Label(self, text="Select the encrypted file").pack(pady=10)
        tk.Button(self, text="Browse File", command=self.browse_file).pack()
        tk.Entry(self, textvariable=self.file_path).pack()

        # Selecionar chave
        tk.Label(self, text="Select the key file").pack(padx=30)
        tk.Button(self, text="Browse File", command=self.browse_key_file).pack()
        tk.Entry(self, textvariable=self.key_path).pack()

        # Confirmar descriptografia
        tk.Button(self, text="Decrypt", command=self.decrypt).pack()


    # Funções
    def show_menu_frame(self):
        self.app_manager.show_frame(self.app_manager.menu_frame)

    def browse_file(self):
        file_selected = filedialog.askopenfilename()
        if file_selected:
            self.file_path.set(file_selected)

    def browse_key_file(self):
        key_file_selected = filedialog.askopenfilename()
        if key_file_selected:
            self.key_path.set(key_file_selected)

    def decrypt_file(self, key, in_filename, out_filename=None, chunksize=24*1024):
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)

    def decrypt(self):
        file_path = self.file_path.get()
        key_path = self.key_path.get()

        if not file_path:
            messagebox.showerror("Error", "Select a folder to decrypt.")
            return

        if not key_path:
            messagebox.showerror("Error", "Select the key file.")
            return

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

            os.remove(file_path)

            messagebox.showinfo("Success", "Folder decrypted successfully.")

        except Exception as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Decryption failed.")