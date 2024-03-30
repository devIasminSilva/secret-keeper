import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#1d1e1f')

        self.app_manager = app_manager

        self.create_widgets()

    def create_widgets(self):
        self.create_background()
        self.create_empty_row()
        self.create_encrypt_button()
        self.create_decrypt_button()

    def create_background(self):
        self.background_image = tk.PhotoImage(file='assets/backgrounds/menu.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

    def create_empty_row(self):
        tk.Label(self, bg='#1d1e1f').grid(row=1, pady=30)

    def create_encrypt_button(self):
        self.encrypt_button = tk.PhotoImage(file='assets/buttons/encrypt.png')
        tk.Button(self, image=self.encrypt_button, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.show_encrypt_frame).grid(row=2, column=0, padx=10)

    def create_decrypt_button(self):
        self.decrypt_button = tk.PhotoImage(file='assets/buttons/decrypt.png')
        tk.Button(self, image=self.decrypt_button, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.show_decrypt_frame).grid(row=2, column=1, padx=10)

    def show_encrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.encrypt_frame)

    def show_decrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.decrypt_frame)
