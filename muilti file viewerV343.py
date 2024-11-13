import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class FileViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Viewer")

        # Setup the menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
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


        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_tab)
        self.file_menu.add_command(label="Open...", command=self.open_file_dialog)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_command(label="Close", command=self.close_tab)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
       
        self.edit_menu.add_command(
            label="Cut",
            accelerator="Ctrl+X",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Cut>>"),
        )
        self.edit_menu.add_command(
            label="Copy",
            accelerator="Ctrl+C",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Copy>>"),
        )
        self.edit_menu.add_command(
            label="Paste",
            accelerator="Ctrl+V",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Paste>>"),
        )
        self.edit_menu.add_command(
            label="---",
            compound="left",
            underline=0,
            command=None
        )
        self.edit_menu.add_command(
            label="---",
            accelerator="Ctrl+Y",
            compound="left",
            underline=0,
            command=None,
        )       

        self.edit_menu.add_command(
            label="Find",
            accelerator="Ctrl+F",
            compound="left",
            underline=0,
            command=lambda: self.findreplace(),
        )
        self.edit_menu.add_command(
            label="Replace",
            accelerator="Ctrl+R",
            compound="left",
            underline=0,
            command=lambda: self.findreplace(),
        )
        self.edit_menu.add_command(
            label="cleartags",
            accelerator="Ctrl+G",
            compound="left",
            underline=0,
            command=lambda: self.cleartags(),
        )


               # Create the Notebook widget
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=1, sticky='nsew')

        # Grid configuration for resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        self.load_filelist()
        self.listbox.bind('<Double-1>', self.open_file)
    def load_filelist(self):
    
        file_extensions = ('.py', '.c', '.log', '.csv', '.json')
        files = [f for f in os.listdir('.') if f.endswith(file_extensions)]
        for file in files:
            self.listbox.insert('end', file)


    def new_tab(self, content="", title="Untitled"):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)

        textwidget = tk.Text(tab, wrap='word', height=15)
        textwidget.grid(row=0, column=0, sticky='nsew')
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        textwidget.insert('1.0', content)
        textwidget.focus_set()


    def open_file(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            file_name = self.listbox.get(index)
            self.create_tab(file_name)


    def create_tab(self, file_name):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=file_name)

        textwidget = tk.Text(tab, wrap='word', height=15)
        textwidget.grid(row=0, column=0, sticky='nsew')
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        with open(file_name, 'r') as file:
            textwidget.insert('1.0', file.read())

        textwidget.bind("<Key>", lambda e: "break")




    def open_file_dialog(self):
        file_name = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if file_name:
            self.create_tab(file_name)

    def save_file(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        textwidget = current_tab.winfo_children()[0]
        file_name = self.notebook.tab(self.notebook.select(), "text")
        
        if file_name == "Untitled":
            self.save_as_file()
        else:
            with open(file_name, 'w') as file:
                file.write(textwidget.get("1.0", "end-1c"))
            messagebox.showinfo("Save", "File saved successfully!")

    def save_as_file(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        textwidget = current_tab.winfo_children()[0]
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        if file_name:
            with open(file_name, 'w') as file:
                file.write(textwidget.get("1.0", "end-1c"))
            self.notebook.tab(self.notebook.select(), text=os.path.basename(file_name))
            messagebox.showinfo("Save", "File saved as: " + file_name)

    def close_tab(self):
        current = self.notebook.select()
        if current:
            self.notebook.forget(current)

    def copy_text(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        textwidget = current_tab.winfo_children()[0]
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(textwidget.selection_get())
        except tk.TclError:
            pass  # No text selected

    def paste_text(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        textwidget = current_tab.winfo_children()[0]
        try:
            textwidget.insert(tk.INSERT, self.root.clipboard_get())
        except tk.TclError:
            pass  # Clipboard does not contain text




 


























# Main window
root = tk.Tk()
root.geometry("800x400")  # Set initial size of the window
app = FileViewerApp(root)
root.mainloop()
