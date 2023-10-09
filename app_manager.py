import tkinter as tk
from menu import MenuFrame
from encryptor import EncryptFrame
from decryptor import DecryptFrame

class AppManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Keeper")
        self.root.geometry("500x300")
        self.root.configure(background='#1d1e1f')

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
