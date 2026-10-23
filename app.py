import tkinter as tk
from pathlib import Path
from tkinter import messagebox # ERROR: messagebox.showerror("Error", "Error info")
from tkinter import filedialog

root = tk.Tk()
root.title("PyDictionary Version 0.01-beta")
root.geometry("1600x900")

# def browsefile
def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select Dictionary File",
        filetypes=(("JSON FIles", "*.json"), ("All FIles", "*.*"))
    )
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)
def load_dictionary():
    path = entry_path.get()
    if Path(path).exists():
        print(f"Successfully loaded: {path}")
    else:
        print("INVALID FILE PATH")
# Create button to open a dictionary .json file
frame = tk.Frame(root)
frame.pack(pady=30)
# text entry field
entry_path = tk.Entry(frame, width=35, font=("Arial", 12))
entry_path.pack(side=tk.LEFT, padx=5)
# browse button
btn_browse = tk.Button(frame, text="Browse...")
btn_browse.pack(side=tk.LEFT, padx=5)
# run button
btn_load = tk.Button(root, text="Open DIctionary", command=load_dictionary, font=("Arial", 11, "bold"))
btn_load.pack(pady=5)

# end
root.mainloop()