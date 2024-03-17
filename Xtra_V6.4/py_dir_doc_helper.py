import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as st
import importlib
import contextlib
import io
import pydoc

class PyDDViewer:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Input for module/class name
        self.entry = tk.Entry(self.root)
        self.entry.grid(row=0, column=2)

        # Text widget to display the documentation
        self.textwidget = st.ScrolledText(self.root, wrap="word", bg="snow", height=40, width=80)
        self.textwidget.grid(row=3, column=1, columnspan=7, rowspan=4)

        # Button to fetch documentation
        self.button = tk.Button(self.root, text="Show Help", command=self.show_help)
        self.button.grid(row=1, column=1)

        # Button to clear text widget
        self.clr_button = tk.Button(self.root, text="Clear", command=self.clear)
        self.clr_button.grid(row=15, column=1)

        # Button to save file
        self.save_btn = tk.Button(self.root, text="Save to File", command=self.save_file)
        self.save_btn.grid(row=14, column=1)

    def clear(self):
        self.textwidget.delete('1.0', tk.END)

    def show_help(self):
        self.textwidget.delete('1.0', tk.END)
        name = self.entry.get()

        try:
            obj = self.resolve_name(name)
        except Exception as e:
            self.textwidget.insert(tk.END, f"Error: {e}\n")
            return

        doc = self.get_doc(obj)
        self.textwidget.insert(tk.END, doc)
        self.textwidget.insert(tk.END, f"\nDirectory of {name}:\n{dir(obj)}\n")

    def resolve_name(self, name):
        if '.' in name:
            module_name, attr_name = name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            return getattr(module, attr_name)
        else:
            return importlib.import_module(name)

    def get_doc(self, obj):
        with contextlib.redirect_stdout(io.StringIO()) as f:
            help(obj)
        return f.getvalue()

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("Python", "py"), ("All Files", "*.*")],
        )
        if filepath:
            with open(filepath, "w") as output_file:
                text = self.textwidget.get(1.0, tk.END)
                output_file.write(text)

