import tkinter as tk
from tkinter import ttk

class FileViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Viewer")

        # Frame for the listbox and scrollbar
        list_frame = tk.Frame(root)
        list_frame.grid(row=0, column=0, sticky='ns')

        # Create the Listbox to list files
        self.listbox = tk.Listbox(list_frame, width=40, height=15)
        self.listbox.grid(row=0, column=0, sticky='nsew')

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Create the Notebook widget
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=1, sticky='nsew')

        # Grid configuration for resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Load files into the Listbox
        self.load_files()

        # Bind double-click event
        self.listbox.bind('<Double-1>', self.open_file)

    def load_files(self):
        import os
        file_extensions = ('.py', '.c', '.log', '.csv', '.json')
        files = [f for f in os.listdir('.') if f.endswith(file_extensions)]
        for file in files:
            self.listbox.insert('end', file)

    def open_file(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            file_name = self.listbox.get(index)
            self.create_tab(file_name)

    def create_tab(self, file_name):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=file_name)

        text_widget = tk.Text(tab, wrap='word', height=15)
        text_widget.grid(row=0, column=0, sticky='nsew')
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        with open(file_name, 'r') as file:
            text_widget.insert('1.0', file.read())

        text_widget.bind("<Key>", lambda e: "break")

# Main window
root = tk.Tk()
root.geometry("800x400")  # Set initial size of the window
app = FileViewerApp(root)
root.mainloop()
