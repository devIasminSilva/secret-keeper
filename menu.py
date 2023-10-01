import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#0d1117')

        self.app_manager = app_manager

        # Botão 'Encypt Folder'
        self.encrypt_button = tk.PhotoImage(file='Assets/Buttons/encrypt_folder.png')
        self.encrypt = tk.Button(self, image=self.encrypt_button, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.show_encrypt_frame).pack(pady=40)
        
        # Botão 'Decrypt File'
        self.decrypt_button = tk.PhotoImage(file='Assets/Buttons/decrypt_file.png')
        self.decrypt = tk.Button(self, image=self.decrypt_button, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.show_decrypt_frame).pack()


    def show_encrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.encrypt_frame)

    def show_decrypt_frame(self):
        self.app_manager.show_frame(self.app_manager.decrypt_frame)