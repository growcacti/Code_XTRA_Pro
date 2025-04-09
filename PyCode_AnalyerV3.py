import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ast
import inspect
import os
import subprocess
import pkg_resources
import sys
import importlib.util


class CodeAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Code Analyzer")
        self.geometry("1000x700")

        # Grid layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # File selection
        self.file_label = tk.Label(self, text="Select a Python file:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.file_entry = tk.Entry(self, width=50)
        self.file_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.analyze_button = tk.Button(self, text="Analyze", command=self.analyze_file)
        self.analyze_button.grid(row=0, column=3, padx=10, pady=10)

        # Notebook for results
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Tabs
        self.indentation_tab = ttk.Frame(self.notebook)
        self.mro_tab = ttk.Frame(self.notebook)
        self.imports_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.indentation_tab, text="Indentation")
        self.notebook.add(self.mro_tab, text="MRO")
        self.notebook.add(self.imports_tab, text="Imports and Dependencies")

        # Treeview widgets for results
        self.indentation_tree = ttk.Treeview(self.indentation_tab, columns=("line", "spaces"), show="headings")
        self.indentation_tree.heading("line", text="Line")
        self.indentation_tree.heading("spaces", text="Spaces")
        self.indentation_tree.pack(expand=1, fill="both", padx=5, pady=5)

        self.mro_tree = ttk.Treeview(self.mro_tab, columns=("class", "mro"), show="headings")
        self.mro_tree.heading("class", text="Class")
        self.mro_tree.heading("mro", text="MRO")
        self.mro_tree.pack(expand=1, fill="both", padx=5, pady=5)

        self.imports_tree = ttk.Treeview(self.imports_tab, columns=("module", "status"), show="headings")
        self.imports_tree.heading("module", text="Module")
        self.imports_tree.heading("status", text="Status")
        self.imports_tree.pack(expand=1, fill="both", padx=5, pady=5)

        # Button for installing missing dependencies
        self.install_button = tk.Button(self.imports_tab, text="Install Missing Dependencies", command=self.install_missing_dependencies)
        self.install_button.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def analyze_file(self):
        file_path = self.file_entry.get()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("Error", "Please select a valid Python file.")
            return

        with open(file_path, "r") as file:
            code = file.read()

        self.analyze_indentation(code)
        self.analyze_mro(code, file_path)
        self.analyze_imports_and_dependencies(code)

    def analyze_indentation(self, code):
        for item in self.indentation_tree.get_children():
            self.indentation_tree.delete(item)

        for i, line in enumerate(code.splitlines(), 1):
            stripped = line.lstrip()
            if stripped and line.startswith(" "):
                indent_level = len(line) - len(stripped)
                self.indentation_tree.insert("", "end", values=(i, indent_level))

    def analyze_mro(self, code, file_path):
        for item in self.mro_tree.get_children():
            self.mro_tree.delete(item)

        try:
            compiled_code = compile(code, file_path, "exec")
            local_vars = {}
            exec(compiled_code, {}, local_vars)

            for obj_name, obj in list(local_vars.items()):
                if inspect.isclass(obj):
                    mro = inspect.getmro(obj)
                    mro_str = " -> ".join(cls.__name__ for cls in mro)
                    self.mro_tree.insert("", "end", values=(obj_name, mro_str))
        except Exception as e:
            messagebox.showerror("MRO Analysis Error", str(e))

    def analyze_imports_and_dependencies(self, code):
        for item in self.imports_tree.get_children():
            self.imports_tree.delete(item)

        try:
            tree = ast.parse(code)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                        self.imports_tree.insert("", "end", values=(alias.name, self.check_dependency(alias.name)))
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module)
                    self.imports_tree.insert("", "end", values=(node.module, self.check_dependency(node.module)))

            self.dependencies = imports
        except Exception as e:
            messagebox.showerror("Import Analysis Error", str(e))

    def check_dependency(self, module):
        if not module:
            return "UNKNOWN"

        # Check built-in modules
        if module in sys.builtin_module_names:
            return "BUILT-IN"

        # Check standard library
        if importlib.util.find_spec(module):
            return "STANDARD LIBRARY"

        # Check installed packages
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        if module.lower() in installed_packages:
            return "INSTALLED"

        return "MISSING"

    def install_missing_dependencies(self):
        missing_dependencies = [self.imports_tree.item(item)["values"][0] for item in self.imports_tree.get_children()
                                if self.imports_tree.item(item)["values"][1] == "MISSING"]

        if not missing_dependencies:
            messagebox.showinfo("No Missing Dependencies", "All dependencies are already installed.")
            return

        try:
            for dependency in missing_dependencies:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
                self.imports_tree.set(dependency, "status", "INSTALLED")
            messagebox.showinfo("Success", "Missing dependencies installed successfully!")
        except Exception as e:
            messagebox.showerror("Installation Error", str(e))


if __name__ == "__main__":
    app = CodeAnalyzerApp()
    app.mainloop()
