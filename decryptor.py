import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct
from Crypto.Cipher import AES

class DecryptFrame(tk.Frame):
    def __init__(self, app_manager):
        super().__init__(app_manager.root, bg='#0d1117')

        self.app_manager = app_manager

        self.file_path = tk.StringVar()
        self.key_path = tk.StringVar()
        self.delete_var = tk.BooleanVar()

        # Procurar arquivo
        self.browse_file_image = tk.PhotoImage(file='Assets/Buttons/browse_file.png')
        tk.Button(self, image=self.browse_file_image, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.browse_file).grid(row=0, column=0, pady=30, sticky=tk.W)
        tk.Entry(self, textvariable=self.file_path, foreground="gray", bg='#0d1117').grid(row = 0, column = 1, columnspan=3, ipadx=50)

        # Procurar chave
        self.browse_key_file_image = tk.PhotoImage(file='Assets/Buttons/browse_key_file.png')
        tk.Button(self, image=self.browse_key_file_image, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.browse_key_file).grid(row=1, column=0, columnspan=3, sticky=tk.SW)
        tk.Entry(self, textvariable=self.key_path, foreground="gray", bg='#0d1117').grid(row=1, column=1, ipadx=50, padx=10)

        # Deletar arquivo após descriptografia
        tk.Checkbutton(self, text="Delete files after decryption", bg='#0d1117', foreground="gray",  activebackground='#0d1117', selectcolor='#0d1117', variable=self.delete_var).grid(row=3, column=0, columnspan=2, sticky=tk.SW, pady=20)


        # Confirmar descriptografia
        self.decrypt_image = tk.PhotoImage(file='Assets/Buttons/decrypt.png')
        tk.Button(self, image=self.decrypt_image, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.decrypt).grid(row=5, column=1, sticky=tk.SW)

        # Voltar ao menu principal
        self.back_image = tk.PhotoImage(file='Assets/Buttons/back.png')
        tk.Button(self, image=self.back_image, bd=0, bg='#0d1117', activebackground='#0d1117', command=self.show_menu_frame).grid(row=5, column=0, sticky=tk.SW)


    # Funções
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
        delete = self.delete_var.get()

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

            if delete:
                os.remove(file_path)
                os.remove(key_path)

            messagebox.showinfo("Success", "Folder decrypted successfully.")

        except Exception as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Decryption failed.")