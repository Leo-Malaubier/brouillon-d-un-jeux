import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk

class DatabaseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.root.geometry("1200x800")  # Définir la taille de la fenêtre ici
        self.filename = None
        self.dbs = {}
        self.current_db = None

        self.create_widgets()

    def create_widgets(self):
        # Créer un cadre pour les boutons en haut
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Boutons pour les actions principales
        self.select_file_button = tk.Button(self.button_frame, text="Select .py File", command=self.select_file)
        self.select_file_button.grid(row=0, column=0, padx=5, pady=5)

        self.new_db_button = tk.Button(self.button_frame, text="New Dictionary", command=self.new_db)
        self.new_db_button.grid(row=0, column=1, padx=5, pady=5)

        self.select_db_label = tk.Label(self.button_frame)
        self.select_db_label.grid(row=0, column=2, padx=5, pady=5)

        self.select_db_menu = tk.StringVar(self.root)
        self.select_db_menu.set("Select a dictionary")
        self.select_db_dropdown = tk.OptionMenu(self.button_frame, self.select_db_menu, "", command=self.select_db)
        self.select_db_dropdown.grid(row=0, column=3, padx=5, pady=5)

        self.add_entry_button = tk.Button(self.button_frame, text="Add Key-Value Pair", command=self.add_entry)
        self.add_entry_button.grid(row=0, column=4, padx=5, pady=5)

        self.save_db_button = tk.Button(self.button_frame, text="Save Database", command=self.save_db)
        self.save_db_button.grid(row=0, column=5, padx=5, pady=5)

        self.load_db_button = tk.Button(self.button_frame, text="Load Database", command=self.load_db)
        self.load_db_button.grid(row=0, column=6, padx=5, pady=5)

        # Ajouter une ligne de séparation
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)

        # Section inférieure pour les entrées avec scrollbar
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.bottom_frame)
        self.v_scrollbar = tk.Scrollbar(self.bottom_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.bottom_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.table_frame.bind("<Configure>", self.on_frame_configure)

        # Liaison des événements de défilement à la molette
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Control-MouseWheel>", self.on_ctrl_mouse_wheel)

        self.entries = []
    def on_mouse_wheel(self, event):
        """Défilement vertical avec la molette."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_ctrl_mouse_wheel(self, event):
        """Défilement horizontal avec Ctrl + molette."""
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def select_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
        if self.filename:
            self.load_db()
            messagebox.showinfo("Selected File", f"Selected file: {self.filename}")

    def new_db(self):
        db_name = simpledialog.askstring("Input", "Enter the name for the new dictionary:")
        if db_name:
            self.dbs[db_name] = {}
            self.update_db_menu()
            self.select_db_menu.set(db_name)
            self.display_db(db_name)  # Afficher le nouveau dictionnaire
            messagebox.showinfo("Success", f"Dictionary '{db_name}' created.")

    def update_db_menu(self):
        menu = self.select_db_dropdown["menu"]
        menu.delete(0, "end")
        for db_name in self.dbs:
            menu.add_command(label=db_name, command=lambda value=db_name: self.select_db(value))
        self.select_db_menu.set("Select a dictionary")

    def select_db(self, db_name):
        self.select_db_menu.set(db_name)
        self.display_db(db_name)  # Afficher le dictionnaire sélectionné

    def add_entry(self, row=None):
        if self.select_db_menu.get() == "Select a dictionary":
            messagebox.showerror("Error", "Please select a dictionary first.")
            return

        if row is None:
            row = len(self.entries)
            key_entry = tk.Entry(self.table_frame)
            key_entry.grid(row=row, column=0, padx=5, pady=5)
            value_entries = []
            for col in range(1, 2):  # Initial column for value
                value_entry = tk.Entry(self.table_frame)
                value_entry.grid(row=row, column=col, padx=5, pady=5)
                value_entries.append(value_entry)
            add_button = tk.Button(self.table_frame, text="+", command=lambda r=row: self.add_value_entry(r))
            add_button.grid(row=row, column=2, padx=5, pady=5)
            self.entries.append((key_entry, value_entries, add_button))
        else:
            self.add_value_entry(row)

    def add_value_entry(self, row):
        key_entry, value_entries, add_button = self.entries[row]
        col = len(value_entries) + 1

        # Supprimer l'ancien bouton "+"
        add_button.grid_forget()

        # Ajouter une nouvelle case de valeur
        value_entry = tk.Entry(self.table_frame)
        value_entry.grid(row=row, column=col, padx=5, pady=5)
        value_entries.append(value_entry)

        # Ajouter un nouveau bouton "+" à la fin de la ligne
        new_add_button = tk.Button(self.table_frame, text="+", command=lambda r=row: self.add_value_entry(r))
        new_add_button.grid(row=row, column=col + 1, padx=5, pady=5)

        # Mettre à jour la référence du bouton "+" dans la liste des entrées
        self.entries[row] = (key_entry, value_entries, new_add_button)

    def save_db(self):
        if not self.filename:
            messagebox.showerror("Error", "Please select a .py file first.")
            return

        if self.current_db is None:
            messagebox.showerror("Error", "Please select a dictionary first.")
            return

        # Clear current dictionary data
        self.dbs[self.current_db] = {}

        for key_entry, value_entries, _ in self.entries:
            key = key_entry.get().strip()
            values = [value_entry.get().strip() for value_entry in value_entries if value_entry.get().strip()]
            if key and values:
                self.dbs[self.current_db][key] = values

        try:
            with open(self.filename, 'w') as file:
                file.write("dbs = {\n")
                for db_name, db in self.dbs.items():
                    file.write(f"    '{db_name}': {{\n")
                    for key, values in db.items():
                        file.write(f"        '{key}': {values},\n")
                    file.write("    },\n")
                file.write("}\n")

            messagebox.showinfo("Success", "Database saved to file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save database: {str(e)}")

    def load_db(self):
        if not self.filename:
            messagebox.showerror("Error", "Please select a .py file.")
            return

        with open(self.filename, 'r') as file:
            content = file.read()
            try:
                exec(content, globals())
                self.dbs = globals().get('dbs', {})
                self.update_db_menu()
                messagebox.showinfo("Success", "Database loaded successfully.")
                if self.dbs:
                    first_db = next(iter(self.dbs))
                    self.select_db_menu.set(first_db)
                    self.display_db(first_db)  # Afficher le premier dictionnaire chargé
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load database: {str(e)}")

    def display_db(self, db_name=None):
        if db_name is None:
            db_name = self.select_db_menu.get()

        if db_name == "Select a dictionary":
            messagebox.showerror("Error", "Please select a dictionary first.")
            return

        self.current_db = db_name

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.entries = []
        db = self.dbs.get(db_name, {})
        for row, (key, values) in enumerate(db.items()):
            key_entry = tk.Entry(self.table_frame)
            key_entry.grid(row=row, column=0, padx=5, pady=5)
            key_entry.insert(0, key)
            value_entries = []
            for col, value in enumerate(values, start=1):
                value_entry = tk.Entry(self.table_frame)
                value_entry.grid(row=row, column=col, padx=5, pady=5)
                value_entry.insert(0, value)
                value_entries.append(value_entry)
            add_button = tk.Button(self.table_frame, text="+", command=lambda r=row: self.add_value_entry(r))
            add_button.grid(row=row, column=len(values) + 1, padx=5, pady=5)
            self.entries.append((key_entry, value_entries, add_button))

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseManager(root)
    root.mainloop()
