import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.ttk import Combobox

class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Application")

        # Dictionnaires pour les couleurs et les éléments de sauvegarde
        self.colors = {
            "a": "brown",  # mur
            "z": "blue",   # entrée/sortie
            "e": "red",    # étage supérieur
            "r": "yellow", # étage inférieur
            "t": "purple", # cave
            "x": "white"
        }
        self.elements = {
            "a": "y",
            "z": "e",
            "e": "t",
            "r": "g",
            "t": "c",
            "x": "x"
        }
        self.default_color = "white"
        self.default_element = "x"

        self.levels = []
        self.current_level = -1
        self.lower_levels = {}

        self.create_widgets()
        self.root.bind("<Key>", self.key_press)

    def create_widgets(self):
        self.row_label = tk.Label(self.root, text="Number of Rows:")
        self.row_label.pack()

        self.row_entry = tk.Entry(self.root)
        self.row_entry.pack()

        self.col_label = tk.Label(self.root, text="Number of Columns:")
        self.col_label.pack()

        self.col_entry = tk.Entry(self.root)
        self.col_entry.pack()

        self.generate_button = tk.Button(self.root, text="Generate Grid", command=self.generate_grid)
        self.generate_button.pack()

        self.save_button = tk.Button(self.root, text="Save to TXT", command=self.save_to_txt, state=tk.DISABLED)
        self.save_button.pack()

        self.add_level_button = tk.Button(self.root, text="Add Level", command=self.add_level, state=tk.DISABLED)
        self.add_level_button.pack()

        self.remove_level_button = tk.Button(self.root, text="Remove Level", command=self.remove_level, state=tk.DISABLED)
        self.remove_level_button.pack()

        self.add_lower_level_button = tk.Button(self.root, text="Save as Lower Level", command=self.save_as_lower_level, state=tk.DISABLED)
        self.add_lower_level_button.pack()

        self.level_selector_label = tk.Label(self.root, text="Select Level:")
        self.level_selector_label.pack()

        self.level_selector = Combobox(self.root, state="readonly")
        self.level_selector.bind("<<ComboboxSelected>>", self.level_selected)
        self.level_selector.pack()

    def generate_grid(self):
        try:
            self.rows = int(self.row_entry.get())
            self.cols = int(self.col_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integers for rows and columns.")
            return

        self.levels = []
        self.current_level = -1
        self.lower_levels = {}
        self.add_level()

        self.save_button.config(state=tk.NORMAL)
        self.add_level_button.config(state=tk.NORMAL)
        self.remove_level_button.config(state=tk.NORMAL)
        self.add_lower_level_button.config(state=tk.NORMAL)

    def create_grid(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        self.cells = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                cell = tk.Label(self.grid_frame, text="", bg=self.default_color, width=4, height=2, borderwidth=1, relief="solid")
                cell.grid(row=r, column=c)
                cell.bind("<Button-1>", lambda event, r=r, c=c: self.cell_click(r, c))
                row.append(cell)
            self.cells.append(row)

    def display_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.current_level >= 0:
                    element = self.levels[self.current_level][r][c]
                    color = next((color for char, color in self.colors.items() if self.elements[char] == element), self.default_color)
                    self.cells[r][c].config(bg=color)

    def cell_click(self, row, col):
        self.selected_cell = (row, col)

    def key_press(self, event):
        if hasattr(self, 'selected_cell') and self.current_level >= 0:
            row, col = self.selected_cell
            color = self.colors.get(event.char)
            element = self.elements.get(event.char)
            if color and element:
                self.cells[row][col].config(bg=color)
                self.levels[self.current_level][row][col] = element

    def add_level(self):
        self.current_level += 1
        new_level = [[self.default_element for _ in range(self.cols)] for _ in range(self.rows)]
        self.levels.append(new_level)
        if self.current_level > 0:
            self.grid_frame.pack_forget()
        self.create_grid()
        self.display_grid()
        self.update_level_selector()

    def remove_level(self):
        if self.current_level >= 0:
            self.levels.pop(self.current_level)
            self.current_level -= 1
            if self.current_level >= 0:
                self.grid_frame.pack_forget()
                self.create_grid()
                self.display_grid()
            else:
                self.grid_frame.pack_forget()
            self.update_level_selector()

    def update_level_selector(self):
        levels = [f"Level {i + 1}" for i in range(len(self.levels))]
        self.level_selector['values'] = levels
        if levels:
            self.level_selector.current(self.current_level)
        else:
            self.level_selector.set("")

    def level_selected(self, event):
        selected_level = self.level_selector.current()
        if selected_level != self.current_level:
            self.current_level = selected_level
            self.grid_frame.pack_forget()
            self.create_grid()
            self.display_grid()

    def save_to_txt(self):
        file_path = simpledialog.askstring("Save File", "Enter the file name (without extension):")
        if not file_path:
            return
        file_path = f"../model/model_element/batiment/{file_path}.txt"

        with open(file_path, "w") as file:
            file.write(f"{self.rows}{self.cols}\n")
            for level_index, level in enumerate(self.levels):
                file.write(f"Level{level_index+1}\n")
                for r in range(self.rows):
                    row_data = []
                    for c in range(self.cols):
                        element = level[r][c]
                        row_data.append(element)
                    file.write("\t".join(row_data)+"\n")
                file.write("\n")

            # Save lower levels
            for level_index, level in self.lower_levels.items():
                file.write(f"Lower Level{level_index}\n")
                for r in range(self.rows):
                    row_data = []
                    for c in range(self.cols):
                        element = level[r][c]
                        row_data.append(element)
                    file.write("\t".join(row_data)+"\n")
                file.write("\n")

        messagebox.showinfo("File Saved", f"Grid data has been saved to {file_path}")

    def save_as_lower_level(self):
        if self.current_level >= 0:
            self.lower_levels[self.current_level] = [row[:] for row in self.levels[self.current_level]]
            messagebox.showinfo("Saved as Lower Level", f"Current level {self.current_level + 1} has been saved as lower level.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    app.update_level_selector()  # Mettre à jour la combobox après la création initiale de l'application
    root.mainloop()
