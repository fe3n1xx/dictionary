import tkinter as tk
import json
import zipfile
from tkinter import ttk
from pathlib import Path
from tkinter import messagebox # ERROR: messagebox.showerror("Error", "Error info")
from tkinter import filedialog

RECENT_FILE = Path("recent_folder.json")

def load_recent_folders():
    if RECENT_FILE.exists():
        try:
            with open(RECENT_FILE, "r", encoding="utf=8") as f:
                return json.load(f)
        except:
            return []
    return []

def add_recent_folder(folder_path):
    recents = load_recent_folders()
    path_str = str(folder_path)
    if path_str in recents:
        recents.remove(path_str)
    recents.insert(0, path_str)
    with open(RECENT_FILE, "w", encoding="utf-8") as f:
        json.dump(recents[:5], f, indent=4)

def load_dictionary_data(project_folder):
    dict_file = project_folder / "dictionary.json"
    if dict_file.exists():
        try:
            with open(dict_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_dictionary_data(data, project_folder):
    dict_file = project_folder / "dictionary.json"
    with open(dict_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4) # 4=tab

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="PyDictionary Launcher v1.10 beta", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        btn_open = tk.Button(self, text="Open Default Dictionary", font=("Arial", 12), command=self.open_default)
        btn_open.pack(pady=5)

        btn_folder = tk.Button(self, text="Open Specific Folder", font=("Arial", 12), bg="#224d73", fg="white", command=self.select_folder)
        btn_folder.pack(pady=5)
        
        tk.Label(self, text="Recent Dictionaries:", font=("Arial", 12, "bold")).pack(pady=(15, 5))

        self.recent_frame = tk.Frame(self)
        self.recent_frame.pack(pady=5)
        self.refresh_recents()
    def refresh_recents(self):
        for widget in self.recent_frame.winfo_children():
            widget.destroy
        recents = load_recent_folders()
        if not recents:
            tk.Label(self.recent_frame, text="No recent dictionaries found.", fg="gray").pack()
            return

        for path in recents:
            p = Path(path)
            if p.exists():
                btn = tk.Button(self.recent_frame, text=p.name, width=35, command=lambda path=p: self.open_specific(path))
                btn.pack(pady=2)
    def open_default(self):
        self.controller.project_folder = Path(".")
        self.controller.show_frame("DictionaryDashboard")
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.open_specific(Path(folder))
    def open_specific(self, folder_path):
        self.controller.project_folder = Path(folder_path)
        add_recent_folder(folder_path)
        self.controller.show_frame("DictionaryDashboard")

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

        tk.Button(top_frame, text="Export .pydict", command=self.export_pydict).pack(side=tk.RIGHT, padx=5)
        tk.Button(top_frame, text="Import .pydict", command=self.import_pydict).pack(side=tk.RIGHT, padx=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.dict_tab = ttk.Frame(self.notebook)
        self.grammar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dict_tab, text="Lexicon")
        self.notebook.add(self.grammar_tab, text="Grammar")

        self.setup_dictionary_tab()
        self.setup_grammar_tab()

    def export_pydict(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pydict", filetypes=[("PyDictionary File", "*.pydict")])
        if not file_path:
            return
        try:
            with zipfile.ZipFile(file_path, 'w') as zf:
                dict_file = self.controller.project_folder / "dictionary.json"
                grammar_file = self.controller.project_folder / "grammar"
                if dict_file.exists():
                    zf.write(dict_file, "dictionary.json")
                if grammar_file.exists():
                    zf.write(grammar_file, "grammar")
            messagebox.showinfo("SUCCESS", f"Dictioary successfully exported")
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to export: {e}")

    def import_pydict(self):
        file_path = filedialog.askopenfilename(filetypes=[("PyDictionary File", "*.pydict")])
        if not file_path:
            return
        target_folder = filedialog.askdirectory(title="Select folder to unpack .pydict to")
        if not target_folder:
            return
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                zf.extractall(target_folder)
            self.controller.project_folder = Path(target_folder)
            add_recent_folder(target_folder)
            self.refresh_dict_display()
            messagebox.showinfo("SUCCESS", "Successfully imported .pydict archive!")
        except Exception as e:
            messagebox.showerror("ERROR", f"FFailed to import: {e}")
    
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
        data = load_dictionary_data(self.controller.project_folder)
        if word in data:
            del data[word]
            save_dictionary_data(data, self.controller.project_folder)
            self.del_word_entry.delete(0, tk.END)
            self.refresh_dict_display()
            messagebox.showinfo("SUCCESS", f"Deleted '{word}'!")
        else:
            messagebox.showerror("ERROR", "Please enter a valid word!")
    def refresh_dict_display(self):
        self.dict_text.delete("1.0", tk.END)
        data = load_dictionary_data(self.controller.project_folder)
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
        data = load_dictionary_data(self.controller.project_folder)
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
        data = load_dictionary_data(self.controller.project_folder)
        data[word] = definition
        save_dictionary_data(data, self.controller.project_folder)
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
    def refresh_data(self):
        folder_name = self.controller.project_folder.resolve()
        self.controller.root.title(f"PyDictionary = Active: {folder_name}")

        self.refresh_dict_display()

        self.grammar_text.delete("1.0", tk.END)

        grammar_file = self.controller.project_folder / "grammar"
        if grammar_file.exists():
            with open(grammar_file, "r", encoding="utf-8") as f:
                rules_text = f.read()
        else:
            rules_text = ""

        self.grammar_text.insert("1.0", rules_text)
class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyDictionary Version 1.10 beta")
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
        if hasattr(frame, "refresh_data"):
            frame.refresh_data()

# run app
if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()