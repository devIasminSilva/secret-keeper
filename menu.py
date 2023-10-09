import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#1d1e1f')

        self.app_manager = app_manager

        # Background
        self.background_image = tk.PhotoImage(file='assets/backgrounds/menu.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Botão 'Encypt'
        self.encrypt_button = tk.PhotoImage(file='assets/buttons/encrypt.png')
        tk.Button(self, image=self.encrypt_button, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.show_encrypt_frame).grid(row=0, column=0, padx=10, pady=190)
        
        # Botão 'Decrypt'
        self.decrypt_button = tk.PhotoImage(file='assets/buttons/decrypt.png')
        tk.Button(self, image=self.decrypt_button, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.show_decrypt_frame).grid(row=0, column=1, padx=10)


        ###### Funções ######

    def show_encrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.encrypt_frame)

    def show_decrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.decrypt_frame)