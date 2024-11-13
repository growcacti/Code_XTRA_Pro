import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class FileViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Viewer")

        # Create the Notebook widget
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Create the Listbox to list files
        self.listbox = tk.Listbox(root, width=40, height=15)
        self.listbox.pack(side='left', fill='y')

        # Frame for Listbox scrollbar
        frame = tk.Frame(root)
        frame.pack(side='left', fill='y')

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')

        self.listbox.config(yscrollcommand=scrollbar.set)

        # Load files into the Listbox
        self.load_files()

        # Bind double-click event
        self.listbox.bind('<Double-1>', self.open_file)

    def load_files(self):
        # Assuming files are in the current directory for simplicity
        import os
        files = [f for f in os.listdir('.') if f.endswith('.txt')]
        for file in files:
            self.listbox.insert('end', file)

    def open_file(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            file_name = self.listbox.get(index)
            self.create_tab(file_name)

    def create_tab(self, file_name):
        # Create a new tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=file_name)

        # Create a Text widget
        text_widget = tk.Text(tab, wrap='word', height=15)
        text_widget.pack(fill='both', expand=True)

        # Load file content
        with open(file_name, 'r') as file:
            text_widget.insert('1.0', file.read())

        # Make text read-only (if desired)
        text_widget.bind("<Key>", lambda e: "break")

# Main window
root = tk.Tk()
app = FileViewerApp(root)
root.mainloop()
