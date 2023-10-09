import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct
from Crypto.Cipher import AES

class DecryptFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#1d1e1f')

        self.app_manager = app_manager

        self.file_path = tk.StringVar()
        self.key_path = tk.StringVar()

        # Background
        self.background_image = tk.PhotoImage(file='assets/backgrounds/bg.png')
        self.background_label = tk.Label(self, image=self.background_image).place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self, text=" ", background='#1d1e1f').grid(row=0, column=0, sticky=tk.W, pady=5)

        # Procurar arquivo
        self.browse_file_image = tk.PhotoImage(file='assets/buttons/select_file.png')
        tk.Button(self, image=self.browse_file_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.browse_file).grid(row=2, column=0, sticky=tk.SW, pady=20, padx=10)
        tk.Entry(self, textvariable=self.file_path, foreground="gray", bg='#1d1e1f', bd=0).grid(row=3, column=0, columnspan=3, sticky=tk.W, ipadx=120, padx=10)

        # Procurar chave
        self.browse_key_file_image = tk.PhotoImage(file='assets/buttons/select_key_file.png')
        tk.Button(self, image=self.browse_key_file_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.browse_key_file).grid(row=4, column=0, sticky=tk.SW, pady=20, padx=10)
        tk.Entry(self, textvariable=self.key_path, foreground="gray", bg='#1d1e1f', bd=0).grid(row=5, column=0, columnspan=3, sticky=tk.W, ipadx=120, padx=10)

        # Confirmar
        self.decrypt_image = tk.PhotoImage(file='assets/buttons/confirm.png')
        tk.Button(self, image=self.decrypt_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.decrypt).grid(row=6, column=0, sticky=tk.SW, pady=50, padx=100)

        # Voltar ao menu
        self.back_image = tk.PhotoImage(file='assets/buttons/back.png')
        tk.Button(self, image=self.back_image, bd=0, bg='#1d1e1f', activebackground='#1d1e1f', cursor="hand2", command=self.show_menu_frame).grid(row=6, column=0, sticky=tk.SW, pady=50, padx=10)


    ###### Funções ######

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

    def decrypt_file(self, key, in_filename, out_filename=None, chunksize=24*1024):
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)

    def decrypt(self):
        file_path = self.file_path.get()
        key_path = self.key_path.get()

        if not file_path:
            messagebox.showerror("Error", "Select a folder to decrypt.")
            return

        if not key_path:
            messagebox.showerror("Error", "Select the key file.")
            return

        try:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()

            out_filename = os.path.splitext(file_path)[0]
            
            with open(file_path, 'rb') as infile:
                origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
                iv = infile.read(16)
                decryptor = AES.new(key, AES.MODE_CBC, iv)

                with open(out_filename, 'wb') as outfile:
                    while True:
                        chunk = infile.read(64*1024)
                        if len(chunk) == 0:
                            break
                        outfile.write(decryptor.decrypt(chunk))

                    outfile.truncate(origsize)

            messagebox.showinfo("Success", "Folder decrypted successfully.")

        except Exception as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Decryption failed.")