import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import os

class FindReplaceApp:
    def __init__(self, parent):
        self.parent = parent
       

        # GUI Components
        self.setup_gui()
    def setup_gui(self):
        # Frame for control widgets
        self.control_frame = tk.Frame(self.parent)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

        # Select Directory Button
        select_button = tk.Button(self.control_frame, text="Select Directory", command=self.select_directory)
        select_button.grid(row=0, column=0, padx=10, pady=5)

        # Directory Label
        self.directory_label = tk.Label(self.control_frame, text="Select a directory", fg="blue")
        self.directory_label.grid(row=1, column=0, padx=10, pady=5)

        # Find and Replace Entries
        self.setup_find_replace_entries()

        # Buttons
        self.setup_buttons()

        # Skip Lines Spinbox
        tk.Label(self.control_frame, text="Skip Lines:").grid(row=6, column=0, sticky='e', padx=10)
        self.skip_lines_spinbox = tk.Spinbox(self.control_frame, from_=0, to=10, width=5)
        self.skip_lines_spinbox.grid(row=6, column=1, padx=10, pady=5)

        # List Box
        self.list_box = Listbox(self.parent, width=80, height=20)
        self.list_box.grid(row=0, column=2, rowspan=6, padx=10, pady=10)


    
        # Find and Replace Entries
        self.setup_find_replace_entries()

        # Buttons
        self.setup_buttons()
       
    def setup_find_replace_entries(self):
        tk.Label(self.control_frame, text="Find:").grid(row=3, column=0, sticky='e', padx=10)
        self.find_entry = tk.Entry(self.control_frame)
        self.find_entry.grid(row=2, column=1, padx=10)

        tk.Label(self.control_frame, text="Replace With:").grid(row=8, column=0, sticky='e', padx=10)
        self.replace_entry = tk.Entry(self.control_frame)
        self.replace_entry.grid(row=8, column=1, padx=10)

    def setup_buttons(self):
        find_button = tk.Button(self.control_frame, text="Find", command=self.find_in_files)
        find_button.grid(row=4, column=1, padx=10, pady=10)
        replace_button = tk.Button(self.control_frame, text="Replace", command=lambda: self.find_in_files(True))
        replace_button.grid(row=9, column=1, padx=10, pady=10)
        skiplines_button = tk.Button(self.control_frame, text="Skip # Line Replace", command=self.skip_line_replace)
        skiplines_button.grid(row=7, column=15, padx=10, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        self.directory_label.config(text=directory)


    def skip_line_replace(self):
        skip_lines = int(self.skip_lines_spinbox.get())
        self.find_in_files(True, skip_lines)

    def find_in_files(self, replace=False, skip_lines=0):
        directory = self.directory_label.cget("text")
        find_word = self.find_entry.get()
        replace_word = self.replace_entry.get() if replace else None

        self.list_box.delete(0, tk.END)  # Clear existing entries in the list box

        for parent, dirs, files in os.walk(directory):
            for file in files:
                
                file_path = os.path.join(parent, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='ISO-8859-1') as f:
                            content = f.read()
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while processing {file_path}: {e}")
                        continue

                count = content.count(find_word)
                if count > 0:
                    if replace and replace_word:
                        content = content.replace(find_word, replace_word)
                        with open(file_path, 'w') as f:
                            f.write(content)
                        self.list_box.insert(tk.END, f"{file}: Replaced {count} occurrences")
                    else:
                        self.list_box.insert(tk.END, f"{file}: Found {count} occurrences")



