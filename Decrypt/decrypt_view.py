import tkinter as tk
from tkinter import filedialog, messagebox
from Decrypt.decrypt_service import DecryptService

class DecryptView(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#1d1e1f')
        self.app_manager = app_manager
        self.decrypt_service = DecryptService()
        self.file_path = tk.StringVar()
        self.key_path = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.create_background()
        self.create_file_input()
        self.create_key_input()
        self.create_confirm_button()
        self.create_back_button()

    def create_background(self):
        self.background_image = tk.PhotoImage(file='assets/backgrounds/bg.png')
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_file_input(self):
        self.browse_file_image = tk.PhotoImage(file='assets/buttons/select_file.png')
        tk.Button(self, image=self.browse_file_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.browse_file).grid(row=1, column=0, sticky=tk.SW, pady=30, padx=10)
        tk.Entry(self, textvariable=self.file_path, foreground="gray", bg='#1d1e1f', bd=0).grid(row=2, column=0, columnspan=3, sticky=tk.W, ipadx=120, padx=10)

    def create_key_input(self):
        self.browse_key_file_image = tk.PhotoImage(file='assets/buttons/select_key_file.png')
        tk.Button(self, image=self.browse_key_file_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.browse_key_file).grid(row=3, column=0, sticky=tk.SW, pady=20, padx=10)
        tk.Entry(self, textvariable=self.key_path, foreground="gray", bg='#1d1e1f', bd=0).grid(row=4, column=0, columnspan=3, sticky=tk.W, ipadx=120, padx=10)

    def create_confirm_button(self):
        self.decrypt_image = tk.PhotoImage(file='assets/buttons/confirm.png')
        tk.Button(self, image=self.decrypt_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.decrypt).grid(row=5, column=0, sticky=tk.SW, pady=40, padx=100)

    def create_back_button(self):
        self.back_image = tk.PhotoImage(file='assets/buttons/back.png')
        tk.Button(self, image=self.back_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.show_menu_frame).grid(row=5, column=0, sticky=tk.SW, pady=40, padx=0)

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

    def decrypt(self):
        file_path = self.file_path.get()
        key_path = self.key_path.get()

        if not file_path:
            messagebox.showerror("Error", "Select a file to decrypt.")
            return

        if not key_path:
            messagebox.showerror("Error", "Select the key file.")
            return

        self.decrypt_service.decrypt_file(file_path, key_path)