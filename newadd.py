import tkinter as tk
from tkinter import filedialog
import os
class PathManagerApp:
    def __init__(self, root):
        self.root = root
    

        # Create widgets
        self.lbpath = tk.Listbox(root)
        self.path_display = tk.Entry(root)

        # Layout using grid
        tk.Button(root, text="Open File", command=self.open_file_dialog).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(root, text="Open Directory", command=self.open_directory_dialog).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Change Directory", command=self.change_directory).grid(row=0, column=2, padx=10, pady=10)
        self.lbpath.grid(row=1, column=0,padx=10, pady=10, sticky="ew")
        tk.Button(root, text="Save Paths", command=self.save_paths).grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        tk.Label(root, text="System Current Directory").grid(row=11, column=0)
        self.path_display.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=12, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(root, text="Update Path", command=self.update_path_display).grid(row=13,column=0)

        # Load the saved paths, if any
        self.load_paths()

    def open_file_dialog(self):
        path = filedialog.askopenfilename(initialdir=self.get_selected_path())
        if path:
            self.lbpath.insert(tk.END, path)

    def open_directory_dialog(self):
        path = filedialog.askdirectory(initialdir=self.get_selected_path())
        if path:
            self.lbpath.insert(tk.END, path)

    def get_selected_path(self):
        selection = self.lbpath.curselection()
        if selection:
            return self.lbpath.get(selection[0])
        return "/"

    def change_directory(self):
        path = self.get_selected_path()
        if path and os.path.isdir(path):
            os.chdir(path)
            self.update_path_display()
            print(f"Current working directory changed to: {path}")

    def save_paths(self):
        with open("paths.txt", "a") as file:
            for path in self.lbpath.get(0, tk.END):
                file.write(path + "\n")

    def load_paths(self):
        try:
            with open("paths.txt", "r") as file:
                for path in file:
                    self.lbpath.insert(tk.END, path.strip())
        except FileNotFoundError:
            pass

    def update_path_display(self):
        self.path_display.delete

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        current = os.getcwd()
        self.root.clipboard_append(current)
        
