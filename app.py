import tkinter as tk
from encryptor import EncryptFrame
from decryptor import DecryptFrame

class AppManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Keeper")
        self.root.geometry("400x200")

        self.current_frame = None

        self.menu_frame = MenuFrame(self)
        self.encrypt_frame = EncryptFrame(self)
        self.decrypt_frame = DecryptFrame(self)

        self.show_frame(self.menu_frame)

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack()

# Menu principal
class MenuFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root)

        self.app_manager = app_manager

        encrypt_folder = tk.Button(self, text="Encrypt Folder", command=self.show_encrypt_frame).pack(ipadx=60, ipady=5, pady=50)
        decrypt_file = tk.Button(self, text="Decrypt File", command=self.show_decrypt_frame).pack(ipadx=68, ipady=5)


    def show_encrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.encrypt_frame)

    def show_decrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.decrypt_frame)