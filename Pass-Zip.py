import tkinter as tk
from tkinter import filedialog, messagebox
import pyzipper
import os

def protect_zip():
    # 1. Select the file
    input_file = filedialog.askopenfilename(title="Select File to Compress")
    if not input_file:
        return

    # 2. Set destination
    output_zip = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("Zip files", "*.zip")],
        title="Save Secure Zip As"
    )
    if not output_zip:
        return

    password = b"SSL-2026" # pyzipper requires password in bytes

    try:
        with pyzipper.AESZipFile(output_zip, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password)
            # Use os.path.basename to avoid storing the full C:\Users\... path inside the zip
            zf.write(input_file, arcname=os.path.basename(input_file))
        
        messagebox.showinfo("Success", "File protected with AES-256 encryption!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Secure Zipper 2026")
root.geometry("300x150")

tk.Label(root, text="AES-256 Password Protection", pady=10).pack()

tk.Button(
    root, 
    text="Select File & Protect", 
    command=protect_zip,
    bg="#0078D7", 
    fg="white",
    padx=10,
    pady=5
).pack(pady=20)

root.mainloop()