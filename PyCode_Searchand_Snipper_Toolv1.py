import os
import re
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox, ttk
import glob
import threading


class EnhancedCodeSearcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Python Code Searcher")
        self.root.geometry("900x750")
        
        # Initialize threading event for cancellation
        self.cancel_event = threading.Event()
        
        # GUI Layout
        tk.Label(root, text="Directory:").grid(row=0, column=0, padx=5, pady=5)
        self.dir_entry = tk.Entry(root,bd=13,bg="aquamarine", width=60)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root,bd=5,bg="plum1", text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=5, pady=5)
        
        self.recursive_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Recursive Search", variable=self.recursive_var).grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Search Options
        self.search_dict_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Search for Dictionaries", variable=self.search_dict_var).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.search_list_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Search for Lists", variable=self.search_list_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.search_tuple_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Search for Tuples", variable=self.search_tuple_var).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.search_set_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Search for Sets", variable=self.search_set_var).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.search_gen_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Search for Generators", variable=self.search_gen_var).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.search_func_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Search for Methods/Functions", variable=self.search_func_var).grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.search_modules_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Search for functools/itertools/collections", variable=self.search_modules_var).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        # Additional Modules Input
        tk.Label(root, text="Additional Modules (comma-separated):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.additional_modules_entry = tk.Entry(root,bd=5,bg="skyblue", width=60)
        self.additional_modules_entry.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Context Lines
        tk.Label(root, text="Lines of Context:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.context_lines_spinbox = tk.Spinbox(root, from_=0, to=100, width=5)
        self.context_lines_spinbox.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        self.context_lines_spinbox.delete(0, tk.END)
        self.context_lines_spinbox.insert(0, "10")
        
        tk.Button(root,bd=8,bg="pale green", text="Search", command=self.start_search).grid(row=8, column=1, padx=5, pady=5)
        tk.Button(root,bd=4,bg="burlywood1", text="Cancel", command=self.cancel_search).grid(row=8, column=2, padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.text_output = ScrolledText(root, bd=13, bg="light cyan", wrap="word")
        self.text_output.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
   
        tk.Button(root,bd=7,bg="pale green", text="Save Results", command=self.save_results).grid(row=12, column=2, padx=5, pady=5)
        tk.Button(root,bd=8,bg="CadetBlue1", text="Clear", command=self.clear).grid(row=12, column=0, padx=5, pady=5)
        self.summary_output = tk.Text(root,bd=15,bg="wheat", wrap="word", height=4)
        self.summary_output.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.summary_output.insert(1.0, "Search Summary: No results yet.")  # Default text
        self.summary_output.config(state="disabled")  # Initially read-only
        
        root.grid_rowconfigure(10, weight=1)
        root.grid_columnconfigure(1, weight=1)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def start_search(self):
       
        self.cancel_event.clear()  # Clear any previous cancel signals
        thread = threading.Thread(target=self.search_files)
        thread.start()
    
    def cancel_search(self):
        self.cancel_event.set()  # Signal the search thread to stop
    
    def search_files(self):
        directory = self.dir_entry.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return
        
        self.text_output.delete(1.0, tk.END)
       
        recursive = self.recursive_var.get()
        context_lines = int(self.context_lines_spinbox.get())
       
        patterns = {}
        if self.search_dict_var.get():
            patterns["Dictionary"] = r"\{.*?\}"
        if self.search_list_var.get():
            patterns["List"] = r"\[.*?\]"
        if self.search_tuple_var.get():
            patterns["Tuple"] = r"\(.*?\)"
        if self.search_set_var.get():
            patterns["Set"] = r"\{.*?\}"
        if self.search_gen_var.get():
            patterns["Generator"] = r"\byield\b"
        if self.search_func_var.get():
            patterns["Method/Function"] = r"\bdef\b\s+\w+"
        if self.search_modules_var.get():
            patterns["Module Use"] = r"\b(functools|itertools|collections)\b"
        
        # Add user-specified modules
        additional_modules = self.additional_modules_entry.get().strip()
        if additional_modules:
            modules = additional_modules.split(",")
            for module in modules:
                module = module.strip()
                if module:
                    patterns[f"Module: {module}"] = rf"\b{module}\b"
        
        results = []
        summary = {}
        file_pattern = "**/*.py" if recursive else "*.py"
        files = list(glob.glob(os.path.join(directory, file_pattern), recursive=recursive))
        
        self.progress_bar["maximum"] = len(files)
        self.progress_bar["value"] = 0
        
        for file_path in files:
            if self.cancel_event.is_set():  # Check if the search was canceled
                self.summary_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, "Search canceled.\n")
                self.summary_output.config(text="Search Summary: Canceled.")
                return

            in_progress = "Search in Progress..........................>"
            self.summary_output.insert(tk.END, in_progress)
            self.progress_bar["value"] += 1
            # progress bar in motion with update below
            self.root.update_idletasks()
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                for i, line in enumerate(lines):
                    for key, pattern in list(patterns.items()):
                        if re.search(pattern, line):
                            start = max(0, i - context_lines)
                            end = min(len(lines), i + context_lines + 1)
                            context = "".join(lines[start:end])
                            result = f"File: {file_path}\nLine: {i+1}\n---------------------------------------\n{context.strip()}\n-----\n"
                            self.text_output.insert(tk.END, result)  # Incremental insertion
                            results.append(result)
                            summary[key] = summary.get(key, 0) + 1
                            self.summary_output.config(state="normal")  # Enable editing
                            self.summary_output.delete(1.0, tk.END)    # Clear previous text
                            if self.results:
                                summary_text = "\n".join([f"{key}: {count} matches" for key, count in list(summary.items())])
                                self.summary_output.insert(1.0, f"Search Summary:\n{summary_text}")
                            else:
                                self.summary_output.insert(1.0, "Search Summary: No matches found.")
                                self.summary_output.config(state="disabled")  # Make read-only again
            except Exception as e:
                result = f"Error reading {file_path}: {e}\n"
                self.text_output.insert(tk.END, result)  # Incremental insertion
                results.append(result)
        
        self.progress_bar["value"] = 0  # Reset progress bar
        if results:
            summary_text = "\n".join([f"{key}: {count} matches" for key, count in list(summary.items())])
            summary = f"Search Summary:\n{summary_text}"
            self.summary_output.insert(tk.END, summary)
        else:
            self.text_output.insert(tk.END, "No matches found.")
            self.summary_output.insert(tk.END, "Search Summary: No matches found.")

    def save_results(self):
        # Get the results from the Text widget
        results = self.text_output.get(1.0, tk.END).strip()
        if not results:
            messagebox.showwarning("Warning", "No results to save.")
            return

        # Open file dialog to save results
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8", errors="ignore") as file:
                    file.write(results)
                messagebox.showinfo("Saved", f"Results saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")


    def clear(self):
        self.text_output.delete(1.0, tk.END)
        self.summary_output.delete(1.0, tk.END)
        
        


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedCodeSearcherApp(root)
    root.mainloop()
