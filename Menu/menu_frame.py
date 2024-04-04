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
        self.encrypt_button_image = tk.PhotoImage(file='assets/buttons/encrypt.png')
        self.encrypt_button = tk.Button(self, image=self.encrypt_button_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.app_manager.switch_to_encrypt_view)
        self.encrypt_button.grid(row=2, column=0, padx=10)

    def create_decrypt_button(self):
        self.decrypt_button_image = tk.PhotoImage(file='assets/buttons/decrypt.png')
        self.decrypt_button = tk.Button(self, image=self.decrypt_button_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.app_manager.switch_to_decrypt_view)
        self.decrypt_button.grid(row=2, column=1, padx=10)