import tkinter as tk
from app import AppManager

def main():
    root = tk.Tk()  
    root.resizable(width=False, height=False)
    root.iconbitmap("icon.ico")
    app = AppManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()