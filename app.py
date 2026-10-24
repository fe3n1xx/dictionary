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

        title = tk.Label(self, text="PyDictionary Launcher v1", font=("Arial", 20, "bold"))
        title.pack(pady=50)

        btn_open = tk.Button(self, text="Open Dictionary", font=("Arial", 14), command=self.attempt_open)
        btn_open.pack(pady=20)

        btn_folder = tk.Button(self, text="Open Specific Folder", font=("Arial", 12), bg="#224d73", fg="white", command=self.select_folder)
        btn_folder.pack(pady=10)
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.controller.project_folder = Path(folder)
            self.controller.show_frame("DictionaryDashboard")

    def attempt_open(self):
        file_path = self.controller.project_folder / "dictionary.json"
        if file_path.exists():
            self.controller.show_frame("DictionaryDashboard")
        else:
            messagebox.showerror("ERROR", "File not found.")

class DictionaryDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 

        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=15, pady=10)

        btn_back = tk.Button(top_frame, text="<- Back to Home", command=lambda: controller.show_frame("WelcomePage"))
        btn_back.pack(side=tk.LEFT)

        title = tk.Label(top_frame, text="Conlang Dictionary Workshop", font=("Arial", 20, "bold"))
        title.pack(side=tk.LEFT, padx=20)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.dict_tab = ttk.Frame(self.notebook)
        self.grammar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dict_tab, text="Lexicon")
        self.notebook.add(self.grammar_tab, text="Grammar")

        self.setup_dictionary_tab()
        self.setup_grammar_tab()

    def setup_dictionary_tab(self):
        left_frame = tk.LabelFrame(self.dict_tab, text="Search & Lexicon", font=("Arial", 11, "bold"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right_frame = tk.LabelFrame(self.dict_tab, text="Add New Word", font=("Arial", 11, "bold"))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=10, pady=10)

        search_box_frame = tk.Frame(left_frame)
        search_box_frame.pack(fill=tk.X, padx=10, pady=10)

        self.search_entry = tk.Entry(search_box_frame, width=18)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_box_frame, text="Search", command=self.search_word).pack(side=tk.LEFT, padx=5)
        tk.Button(search_box_frame, text="Show All", command=self.refresh_dict_display).pack(side=tk.LEFT, padx=5)

        self.dict_text = tk.Text(left_frame, height=15, width=40)
        self.dict_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(right_frame, text="Word:").pack(anchor="w", padx=10, pady=(10,0))
        self.add_word_entry = tk.Entry(right_frame, width=20)
        self.add_word_entry.pack(anchor="w", padx=10, pady=5)

        tk.Label(right_frame, text="Definition:").pack(anchor="w", padx=10, pady=(10,0))
        self.add_def_text = tk.Text(right_frame, height=5, width=20)
        self.add_def_text.pack(anchor="w", padx=10, pady=5)

        tk.Button(right_frame, text="Add to Lexicon", bg="#10DB10", fg="white", command=self.add_word).pack(anchor="w", padx=10, pady=10)

        tk.Label(right_frame, text="Delete Word:").pack(anchor="w", padx=10, pady=(15,0))
        self.del_word_entry = tk.Entry(right_frame, width=20)
        self.del_word_entry.pack(anchor="w", padx=10, pady=(15,0))

        tk.Button(right_frame, text="Delete Word", bg="#e00a0a", fg="white", command=self.delete_word).pack(anchor="w", padx=10, pady=5)

        self.refresh_dict_display()
    def delete_word(self):
        word = self.del_word_entry.get().strip()
        if not word:
            messagebox.showerror("ERROR", "Please enter a valid word!")
            return
        data = load_dictionary_data()
        if word in data:
            del data[word]
            save_dictionary_data(data)
            self.del_word_entry.delete(0, tk.END)
            self.refresh_dict_display()
            messagebox.showinfo("SUCCESS", f"Deleted '{word}'!")
        else:
            messagebox.showerror("ERROR", "Please enter a valid word!")
    def refresh_dict_display(self):
        self.dict_text.delete("1.0", tk.END)
        data = load_dictionary_data()
        if not data:
            self.dict_text.insert(tk.END, "Dictionary is Empty.")
            return
        for word, definition in sorted(data.items()):
            self.dict_text.insert(tk.END, f"• {word}\n{definition}\n\n")

    def search_word(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.refresh_dict_display()
            return
        data = load_dictionary_data()
        self.dict_text.delete("1.0", tk.END)
        found = False
        for word, definition in sorted(data.items(), key=lambda x: x[0].lower()):
            if query in word.lower() or query in definition.lower():
                self.dict_text.insert(tk.END, f"• {word} (Match)\n {definition}\n\n")
                found = True
        if not found:
            self.dict_text.insert(tk.END, f"No matches found for '{query}'.")

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

        tk.Label(grammar_frame, text="Edit Grammar Guidelines", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))

        self.grammar_text = tk.Text(grammar_frame, height=15, width= 60, font=("Arial", 11))
        self.grammar_text.pack(fill=tk.BOTH, expand=True, pady=5)

        grammar_file = self.controller.project_folder / "grammar"
        if grammar_file.exists():
            with open(grammar_file, "r", encoding="utf-8") as f:
                rules_text = f.read()
        else:
            rules_text = ""

        self.grammar_text.insert("1.0", rules_text)

        tk.Button(grammar_frame, text="Save Grammar Rules", bg="#10DB10", fg="white", command=self.save_grammar).pack(anchor="w", pady=10)
    def save_grammar(self):
        rules_text = self.grammar_text.get("1.0", tk.END).strip()
        with open("grammar", "w", encoding="utf-8") as f:
            f.write(rules_text)
        messagebox.showinfo("SUCCESS", "Grammar Rules saved successfully!")
class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyDictionary Version 1.00")
        self.root.geometry("1600x900")

        self.project_folder = Path(".")

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