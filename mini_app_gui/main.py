import tkinter as tk
from summary import generate_summary
 
def calculate():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
 
        s, m = generate_summary(a, b)
        result_label.config(
            text=f"Sum: {s}\nProduct: {m}"
        )
    except ValueError:
        result_label.config(text="Please enter valid numbers")
 
# Create window
root = tk.Tk()
root.title("Mini App GUI")
root.geometry("300x220")
 
# UI Elements
tk.Label(root, text="Enter first number").pack(pady=5)
entry_a = tk.Entry(root)
entry_a.pack()
 
tk.Label(root, text="Enter second number").pack(pady=5)
entry_b = tk.Entry(root)
entry_b.pack()
 
tk.Button(root, text="Calculate", command=calculate).pack(pady=10)
 
result_label = tk.Label(root, text="", font=("Arial", 11))
result_label.pack(pady=10)
 
# Start app
root.mainloop()