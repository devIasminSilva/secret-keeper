import tkinter as tk
from Encrypt.encrypt_view import EncryptView
from Decrypt.decrypt_view import DecryptView
from Menu.menu_frame import MenuFrame

class AppManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Keeper")
        self.root.geometry("500x300")
        self.root.configure(background='#1d1e1f')

        self.current_frame = None
        self.encrypt_view = EncryptView(self)
        self.decrypt_view = DecryptView(self)
        self.menu_frame = MenuFrame(self)

        self.show_frame(self.menu_frame)

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.place_forget()
        self.current_frame = frame
        self.current_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def switch_to_encrypt_view(self):
        self.show_frame(self.encrypt_view)

    def switch_to_decrypt_view(self):
        self.show_frame(self.decrypt_view)

def main():
    root = tk.Tk()
    app_manager = AppManager(root)
    root.resizable(width=False, height=False)
    root.iconbitmap('assets/icon.ico')
    root.mainloop()

if __name__ == "__main__":
    main()