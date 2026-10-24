import tkinter as tk
import json
from tkinter import ttk
from pathlib import Path
from tkinter import messagebox # ERROR: messagebox.showerror("Error", "Error info")
from tkinter import filedialog
DICTIONARY_FILE = Path("dictionary.json")

def load_dictionary_data():
    if DICTIONARY_FILE.exists():
        try:
            with open(DICTIONARY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_dictionary_data(data):
    with open(DICTIONARY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4) # 4=tab

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="PyDictionary Launcher", font=("Arial", 20, "bold"))
        title.pack(pady=50)

        btn_open = tk.Button(self, text="Open Dictionary", font=("Arial", 14), command=self.attempt_open)
        btn_open.pack(pady=20)

    def attempt_open(self):
        file_path = Path("dictionary.json") # for testing, turn into an input
        if file_path.exists():
            self.controller.show_frame("DictionaryDashboard")
        else:
            messagebox.showerror("ERROR", "File not found.")

class DictionaryDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 

        title = tk.Label(self, text="Conlang Dictionary Workshop", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        self.notebook=ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.dict_tab = ttk.Frame(self.notebook)
        self.grammar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dict_tab, text="Lexicon")
        self.notebook.add(self.grammar_tab, text="Grammar")

        self.setup_dictionary_tab()
        self.setup_grammar_tab()

    def setup_dictionary_tab(self):
        left_frame = tk.LabelFrame(self.dict_tab, text="Search", font=("Arial", 11, "bold"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)

        search_box_frame = tk.Frame(left_frame)
        search_box_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_box_frame, width=18)
        self.search_entry = tk.Entry(search_box_frame, width=18)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_box_frame, text="Search", command=self.search_word).pack(side=tk.LEFT, padx=5)
        tk.Button(search_box_frame, text="Show All", command=self.refresh_dict_display).pack(side=tk.LEFT, padx=5)

        self.dict_text = tk.Text(left_frame, height=15, width=40)
        self.dict_text.pack(anchor="w", padx=10, pady=5)

        tk.Label(right_frame, text="Word:").pack(anchor="w", padx=10, pady=(10,0))
        self.add_word_entry = tk.Entry(right_frame, width=20)
        self.add_word_entry.pack(anchor="w", padx=10, pady=5)

        tk.Button(right_frame, text="Add to Lexicon", bg="#224d73", fg="white", command=self.add_word).pack(anchor="w", padx=10, pady=(10,0))

        self.refresh_dict_display()
        def refresh_dict_display(self):
            self.dict_text.delete("1.0", tk.END)
            data = load_dictionary_data()
            if not data:
                self.dict_text.insert(tk.END, "Dictionary is Empty.")
            for word, definition in data.items():
                self.dict_text.insert(tk.END, f"{word}\n{definition}")
        def search_Word(self):
            query = self.search_entry.get().strip().lower()
            if not query:
                self.refresh_dict_display()
                return
            data = load_dictionary_data()
            self.dict_text.delete("1.0", tk.END)
            found = False
            for word, definition in data.items():
                if query in word.lower() or query in definition.lower():
                    self.dict_text.insert(tk.END, f"{word} (Match)\n {definition}\n\n")
                    found = True
            if not found:
                self.dict_text.insery(tk.END, f"No matches found for '{query}'.")
        def add_word(self):
            word = self.add_word_entry.get().strip()
            definition = self.add_def_text.get("1.0", tk.END).strip()
            if not word or not definition:
                messagebox.showerror("ERROR", "Fill out both fields!")
                return
            data = load_dictionary_data()
            data[word] = definition
            save_dictionary_data(data)
            self.add_word_entry.delete(0, tk.END)
            self.add_def_text.delete("1.0", tk.END)
            self.refresh_dict_display()
            messagebox.showinfo("SUCCESS", f"Added '{word}'!")

        def setup_grammar_tab(self):
            grammar_frame = tk.Frame(self.grammar_tab)
            grammar_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            tk.Label(grammar_frame, text="Grammar Guidelines", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 15))

            rules = [
                "Word Order: SVO",
                "Noun Classes: Animate and Inanimate",
                "Verb Tenses: Past (Default), Present (fl/fla-), Future (pl-/pla-), Active (lj-/lja-), Reccuring (kl-/kla-)"
            ]
            for rule in rules:
                tk.Label(grammar_frame, text=rule, font=("Arial", 11), anchor="w").pack(anchor="w", pady=5)


        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=15, pady=10)

        btn_back = tk.Button(top_frame, text="<- Back to Home", command=lambda: controller.show_frame("WelcomePage"))
        btn_back.pack(side=tk.LEFT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.dict_tab = ttk.Frame(self.notebook)
        self.grammar_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.dict_tab, text="Lexicon")
        self.notebook.add(self.grammar_tab, text="Grammar")

        self.setup_dictionary_tab()
        self.setup_grammar_tab()

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyDictionary Version 0.01-beta")
        self.root.geometry("1600x900")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        container = tk.Frame(self.root) # old breakpoint (self,root)
        container.grid(row=0, column=0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        # register pages
        for PageClass in (WelcomePage, DictionaryDashboard):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WelcomePage")
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# run app
if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()