import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import secrets
import os
import struct
from Crypto.Cipher import AES

class EncryptFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#1d1e1f')

        self.app_manager = app_manager

        self.folder_path = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar()
        self.show_password.set(False)

        self.create_widgets()

    def create_widgets(self):
        self.create_background()
        self.create_folder_input()
        self.create_password_input()
        self.create_toggle_password_button()
        self.create_confirm_button()
        self.create_back_button()

    def create_background(self):
        self.background_image = tk.PhotoImage(file='assets/backgrounds/bg.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_folder_input(self):
        self.browse_folder_image = tk.PhotoImage(file='assets/buttons/select_folder.png')
        tk.Button(self, image=self.browse_folder_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.browse_folder).grid(row=1, column=0, sticky=tk.SW, pady=30, padx=10)
        tk.Entry(self, textvariable=self.folder_path, foreground='gray', bg='#1d1e1f', bd=0).grid(row=2, column=0, columnspan=3, sticky=tk.W, ipadx=120, padx=10)

    def create_password_input(self):
        self.generate_password_image = tk.PhotoImage(file='assets/buttons/generate_password.png')
        tk.Button(self, image=self.generate_password_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.generate_password).grid(row=3, column=0, sticky=tk.SW, pady=25, padx=10)
        self.password_entry = tk.Entry(self, textvariable=self.password, foreground='gray', bg='#1d1e1f', bd=0, show='•')
        self.password_entry.grid(row=4, column=0, columnspan=3, sticky=tk.W, ipadx=120, padx=10, pady=0)

    def create_toggle_password_button(self):
        self.show_password_image = tk.PhotoImage(file='assets/buttons/show.png')
        self.hide_password_image = tk.PhotoImage(file='assets/buttons/hide.png')
        self.toggle_password_button = tk.Button(self, image=self.show_password_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.toggle_password)
        self.toggle_password_button.grid(row=4, column=2, sticky=tk.W, padx=(0, 10))  # Adiciona um espaço à direita

    def create_confirm_button(self):
        self.confirm_image = tk.PhotoImage(file='assets/buttons/confirm.png')
        tk.Button(self, image=self.confirm_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.encrypt).grid(row=5, column=0, sticky=tk.SW, pady=40, padx=100)

    def create_back_button(self):
        self.back_image = tk.PhotoImage(file='assets/buttons/back.png')
        tk.Button(self, image=self.back_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.show_menu_frame).grid(row=5, column=0, sticky=tk.SW, pady=40, padx=0)

    def show_menu_frame(self):
        self.app_manager.show_frame(self.app_manager.menu_frame)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def generate_password(self):
        password = secrets.token_hex(16)
        self.password.set(password)

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.config(show='•')
            self.toggle_password_button.config(image=self.show_password_image)
        else:
            self.password_entry.config(show='')
            self.toggle_password_button.config(image=self.hide_password_image)

        self.show_password.set(not self.show_password.get())

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

            key_filename = folder_path + ".key"
            with open(key_filename, 'wb') as key_file:
                key_file.write(key)

            os.remove(zip_filename)

            messagebox.showinfo("Success", "Folder encrypted successfully. Remember to store the encryption key securely.")

        except Exception as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Encryption failed.")