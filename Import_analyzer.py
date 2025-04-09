import ast
import os
import pkg_resources
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import inspect
import modulefinder
import importlib

# Add a new tab for module details
class DependencyScanner:
    def __init__(self, directory=None, file_path=None):
        self.directory = directory
        self.file_path = file_path
        self.imports = {}
        self.classes_methods = {}
        self.display_library_info()

    def scan_directory(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)
        except (SyntaxError, IndentationError) as e:
            print(f"Error parsing {file_path}: {e}")
            return [], {}

        imports = []
        classes_methods = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    Sclasses_methods[node.name] = methods

            return imports, classes_methods

    def scan_file(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    imports, classes_methods = self.scan_file(file_path)
                    self.imports[file_path] = imports
                    self.classes_methods[file_path] = classes_methods

    def scan_single_file(self, file_path):
        imports, classes_methods = self.scan_file(file_path)
        self.imports[file_path] = imports
        self.classes_methods[file_path] = classes_methods

    def get_dependencies(self):
        dependencies = {}
        for file, imports in self.imports.items():
            deps = []
            for module in imports:
                try:
                    dist = pkg_resources.get_distribution(module)
                    deps.append((module, dist.version))
                except pkg_resources.DistributionNotFound:
                    deps.append((module, "Not Installed"))
            dependencies[file] = deps
        return dependencies

    def get_module_details(self, module_name):
        """ Return a dictionary of functions, classes, and other information using inspect and dir """
        module_info = {}
        try:
            # Try importing the module
            module = importlib.import_module(module_name)
            
            # Get functions
            functions = [f[0] for f in inspect.getmembers(module, inspect.isfunction)]
            classes = [cls[0] for cls in inspect.getmembers(module, inspect.isclass)]
            attributes = dir(module)  # Get all attributes of the module
            
            module_info['functions'] = functions
            module_info['classes'] = classes
            module_info['attributes'] = attributes
        except ImportError:
            module_info['error'] = f"Module {module_name} could not be imported."

        return module_info
    def display_library_info(self):
        if not self.scanner:
            return

        self.lib_info_tab_text.delete(1.0, tk.END)  # Clear the text widget if any previous content exists
        dependencies = self.scanner.get_dependencies()

        for file, imports in self.scanner.imports.items():
            self.lib_info_tab_text.insert(tk.END, f"File: {file}\n")
            for module_name in imports:
                try:
                    dist = pkg_resources.get_distribution(module_name)
                    self.lib_info_tab_text.insert(tk.END, f"  {module_name} - Version: {dist.version}\n")
                except pkg_resources.DistributionNotFound:
                    self.lib_info_tab_text.insert(tk.END, f"  {module_name} - Not Installed\n")

            self.lib_info_tab_text.insert(tk.END, "\n")




    def scan_file(self, file_path):
        indentation_levels = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_no, line in enumerate(lines, start=1):
                stripped = line.lstrip()
                if stripped:  # Ignore empty lines
                    indent_level = len(line) - len(stripped)
                    indentation_levels.append((line_no, indent_level))
        except (SyntaxError, IndentationError) as e:
            print(f"Error parsing {file_path}: {e}")
            return [], {}, []

        imports = []
        classes_methods = {}
        for node in ast.walk(tree):
            # Existing logic for imports, classes, and methods
            indent_scan()
        return imports, classes_methods, indentation_levels



    def display_library_info(self):
        # Ensure there is valid data to display
        if not self.imports:
            return

        self.lib_info_tab_text.delete(1.0, tk.END)  # Clear the text widget if any previous content exists
        dependencies = self.get_dependencies()

        for file, imports in self.imports.items():
            self.lib_info_tab_text.insert(tk.END, f"File: {file}\n")
            for module_name in imports:
                try:
                    dist = pkg_resources.get_distribution(module_name)
                    self.lib_info_tab_text.insert(tk.END, f"  {module_name} - Version: {dist.version}\n")
                except pkg_resources.DistributionNotFound:
                    self.lib_info_tab_text.insert(tk.END, f"  {module_name} - Not Installed\n")

            self.lib_info_tab_text.insert(tk.END, "\n")

    def indent_scan(self):
        f.write("\nIndentation Levels:\n")
        for file, indentations in self.scanner.indentation_levels.items():
            f.write(f"\nFile: {file}\n")
            for line_no, level in indentations:
                f.write(f"  Line {line_no}: {level} spaces\n")










class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dependency Scanner")
        self.geometry("800x600")

        # Initialize Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.directory_tab = ttk.Frame(self.notebook)
        self.hierarchy_tab = ttk.Frame(self.notebook)
        self.module_info_tab = ttk.Frame(self.notebook)
        self.lib_info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.directory_tab, text="Directory Structure")
        self.notebook.add(self.hierarchy_tab, text="Hierarchy")
        self.notebook.add(self.module_info_tab, text="Module Info")
        self.notebook.add(self.lib_info_tab, text="Library Info")

        # Directory tab widgets
        self.scan_type_label = ttk.Label(self.directory_tab, text="Select Scan Type:")
        self.scan_type_label.pack(anchor="nw", padx=10, pady=5)

        self.scan_type_var = tk.StringVar(value="directory")
        self.directory_radio = ttk.Radiobutton(self.directory_tab, text="Directory", variable=self.scan_type_var, value="directory")
        self.file_radio = ttk.Radiobutton(self.directory_tab, text="Single File", variable=self.scan_type_var, value="file")

        self.directory_radio.pack(anchor="nw", padx=10, pady=5)
        self.file_radio.pack(anchor="nw", padx=10, pady=5)

        self.directory_label = ttk.Label(self.directory_tab, text="Select a Directory or File:")
        self.directory_label.pack(anchor="nw", padx=10, pady=5)

        self.directory_entry = ttk.Entry(self.directory_tab, width=60)
        self.directory_entry.pack(anchor="nw", padx=10, pady=5)
        
        self.browse_button = ttk.Button(self.directory_tab, text="Browse", command=self.browse_directory_or_file)
        self.browse_button.pack(anchor="nw", padx=10, pady=5)
        
        self.scan_button = ttk.Button(self.directory_tab, text="Scan", command=self.scan_directory_or_file)
        self.scan_button.pack(anchor="nw", padx=10, pady=5)

        self.directory_tree = ttk.Treeview(self.directory_tab)
        self.directory_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Hierarchy tab widgets
        self.hierarchy_tree = ttk.Treeview(self.hierarchy_tab)
        self.hierarchy_tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Module Info tab widgets
        self.module_info_label = ttk.Label(self.module_info_tab, text="Module Details will appear here")
        self.module_info_label.pack()

        # Lib Info tab widgets
        self.lib_info_label = ttk.Label(self.lib_info_tab, text="Library Info will appear here")
        self.lib_info_label.pack()

        # Save button
        self.save_button = ttk.Button(self, text="Save Results", command=self.save_results)
        self.save_button.pack(side="bottom", pady=10)

        self.scanner = None

    def browse_directory_or_file(self):
        if self.scan_type_var.get() == "directory":
            directory = filedialog.askdirectory()
            if directory:
                self.directory_entry.delete(0, tk.END)
                self.directory_entry.insert(0, directory)
        else:
            file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
            if file_path:
                self.directory_entry.delete(0, tk.END)
                self.directory_entry.insert(0, file_path)

    def scan_directory_or_file(self):
        selected_path = self.directory_entry.get()
        if self.scan_type_var.get() == "directory":
            if not os.path.isdir(selected_path):
                messagebox.showerror("Error", "Please select a valid directory.")
                return
            self.scanner = DependencyScanner(directory=selected_path)
            self.scanner.scan_directory()
            self.display_directory_structure(selected_path)
        else:
            if not os.path.isfile(selected_path):
                messagebox.showerror("Error", "Please select a valid Python file.")
                return
            self.scanner = DependencyScanner(file_path=selected_path)
            self.scanner.scan_single_file(selected_path)
        
        self.display_hierarchy()

    def display_directory_structure(self, directory):
        self.directory_tree.delete(*self.directory_tree.get_children())
        for root, dirs, files in os.walk(directory):
            parent = self.directory_tree.insert("", "end", text=root, open=True)
            for file in files:
                if file.endswith(".py"):
                    self.directory_tree.insert(parent, "end", text=file)

    def display_hierarchy(self):
        self.hierarchy_tree.delete(*self.hierarchy_tree.get_children())
        if not self.scanner:
            return

        for file, classes_methods in self.scanner.classes_methods.items():
            parent = self.hierarchy_tree.insert("", "end", text=file, open=True)
            for class_name, methods in classes_methods.items():
                class_item = self.hierarchy_tree.insert(parent, "end", text=class_name, open=True)
                for method in methods:
                    self.hierarchy_tree.insert(class_item, "end", text=method)

    def display_module_info(self, module_name):
        module_details = self.scanner.get_module_details(module_name)

        info = f"Module: {module_name}\n"
        if 'error' in module_details:
            info += module_details['error']
        else:
            info += f"Functions: {', '.join(module_details['functions'])}\n"
            info += f"Classes: {', '.join(module_details['classes'])}\n"
            info += f"Attributes: {', '.join(module_details['attributes'])}\n"

        self.module_info_label.config(text=info)

    def save_results(self):
        if not self.scanner:
            messagebox.showerror("Error", "No results to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not save_path:
            return

        dependencies = self.scanner.get_dependencies()
        with open(save_path, "w", encoding="utf-8") as f:
            f.write("Imports:\n")
            for file, imports in self.scanner.imports.items():
                f.write(f"\nFile: {file}\n")
                f.write("\n".join(imports) + "\n")

            f.write("\nClasses and Methods:\n")
            for file, classes_methods in self.scanner.classes_methods.items():
                f.write(f"\nFile: {file}\n")
                for class_name, methods in classes_methods.items():
                    f.write(f"  Class: {class_name}\n")
                    for method in methods:
                        f.write(f"    Method: {method}\n")

            f.write("\nDependencies:\n")
            for file, deps in dependencies.items():
                f.write(f"\nFile: {file}\n")
                for dep, version in deps:
                    f.write(f"  {dep}: {version}\n")

        messagebox.showinfo("Success", "Results saved successfully.")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
