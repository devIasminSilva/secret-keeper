import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import secrets
import os
import struct
from Crypto.Cipher import AES

class EncryptFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#0d1117')

        self.app_manager = app_manager

        self.folder_path = tk.StringVar()
        self.password = tk.StringVar()
        self.delete_var = tk.BooleanVar()

        
        # Procurar pasta
        self.browse_folder_image = tk.PhotoImage(file='Assets/Buttons/browse_folder.png')
        tk.Button(self, image=self.browse_folder_image, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.browse_folder).grid(row=0, column=0, sticky=tk.W, pady=30)
        tk.Entry(self, textvariable=self.folder_path, foreground='gray', bg='#0d1117').grid(row=0, column=1, columnspan=3, ipadx=50)

        # Gerar senha
        self.password_image = tk.PhotoImage(file='Assets/Buttons/password.png')
        tk.Button(self, image=self.password_image, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.generate_password).grid(row=1, column=0, columnspan=3, sticky=tk.SW)
        tk.Entry(self, textvariable=self.password, foreground='gray', bg='#0d1117').grid(row=1, column=1, ipadx=50, padx=10)

        # Deletar pasta após criptografia
        tk.Checkbutton(self, text="Delete folder after encryption", bg='#0d1117', foreground='gray',  activebackground='#0d1117', selectcolor='#0d1117', variable=self.delete_var).grid(row=3, column=0, columnspan=2, sticky=tk.SW, pady=20)

        # Confirmar criptografia
        self.encrypt_image = tk.PhotoImage(file='Assets/Buttons/encrypt.png')
        tk.Button(self, image=self.encrypt_image, bd=0, bg='#0d1117', activebackground='#0d1117',command=self.encrypt).grid(row=5, column=1, sticky=tk.SW)

        # Voltar ao menu principal
        self.back_image = tk.PhotoImage(file='Assets/Buttons/back.png')
        tk.Button(self, image=self.back_image, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.show_menu_frame).grid(row=5, column=0, sticky=tk.SW)

    # Funções
    def show_menu_frame(self):
        self.app_manager.show_frame(self.app_manager.menu_frame)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def generate_password(self):
        password = secrets.token_hex(16)  
        self.password.set(password)

    def encrypt_file(self, key, in_filename, out_filename=None, chunksize=64*1024):
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

    def encrypt(self):
        folder_path = self.folder_path.get()
        password = self.password.get()
        delete = self.delete_var.get()

        if not folder_path:
            messagebox.showerror("Error", "Please select a folder to encrypt.")
            return

        if not password:
            messagebox.showerror("Error", "Please enter the password.")
            return

        bufferSize = 1024*1024

        try:
            key = secrets.token_bytes(32)

            zip_filename = folder_path + ".zip"
            shutil.make_archive(folder_path, 'zip', folder_path)
            self.encrypt_file(key=key, in_filename=zip_filename, out_filename=zip_filename + ".enc", chunksize=bufferSize)

            # Salva a chave em um arquivo separado
            key_filename = folder_path + ".key"
            with open(key_filename, 'wb') as key_file:
                key_file.write(key)

            os.remove(zip_filename)

            if delete:
                shutil.rmtree(folder_path)

            messagebox.showinfo("Success", "Folder encrypted successfully. Remember to store the encryption key securely.")

        except Exception as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Encryption failed.")