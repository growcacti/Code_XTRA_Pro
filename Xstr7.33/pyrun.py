import tkinter as tk
from tkinter import filedialog
import runpy
import subprocess
class Pyscript_Run:
    def __init__(self,textwidget):
        
        self.textwidget = textwidget
        self.run_python_file
             
    def run_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.textwidget.delete(1.0, tk.END)  # Clear the text widget
            try:
                # Attempt to run the script
                runpy.run_path(file_path)
                # If no exception, append a success message
                self.textwidget.insert(tk.END, "Script executed successfully.\n")
            except Exception as e:
                # If an error occurs, display it in the text widget
                self.textwidget.insert(tk.END, f"An error occurred: {e}\n")

    def run_subprocess(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.textwidget.delete(1.0, tk.END)  # Clear the text widget
            try:
                result = subprocess.run(["python", file_path], capture_output=True, text=True, check=True)
                self.textwidget.insert(tk.END, "Script executed successfully.\n")
                self.textwidget.insert(tk.END, result.stdout)
                if result.stderr:
                    self.textwidget.insert(tk.END, f"Errors:\n{result.stderr}")
            except subprocess.CalledProcessError as e:
                self.textwidget.insert(tk.END, f"An error occurred: {e}\n")  
