import autopep8
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

import os
class AutoPEP8Formatter(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.wtext = tk.Text(self.parent, height=10)
        self.wtext.grid(row=10, column=3)
        self.initUI()
        self.current_directory = os.getcwd()

    def initUI(self):
        tk.Label(self.parent,text = "AutoPEP8 Formatter").grid(row=0 ,column=3)

        self.select_button = tk.Button(self.parent, text="Select Directory", command=self.select_directory)
        self.select_button.grid(row=1, column=1)

        self.file_listbox = tk.Listbox(self.parent)
        self.file_listbox.grid(row=2, column=1)

        self.format_button = tk.Button(self.parent, text="Format Selected File", command=self.format_selected_file)
        self.format_button.grid(row=6, column=3)

     
        

    def select_directory(self):
        self.current_directory = filedialog.askdirectory()
        if self.current_directory:
            self.file_listbox.delete(0, tk.END)
            self.wtext.delete(1.0, tk.END)

            for filename in sorted(os.listdir(self.current_directory)):
                if filename.endswith('.py'):
                    self.file_listbox.insert(tk.END, filename)

    def format_selected_file(self):
        if not self.current_directory:
           mb.showinfo("Info", "Please select a directory first.")
           return

        selected = self.file_listbox.curselection()
        if not selected:
           mb.showinfo("Info", "Please select a file to format.")
           return

        filename = self.file_listbox.get(selected[0])
        file_path = os.path.join(self.current_directory, filename)

        keep_original =mb.askyesno("Keep Original", "Do you want to keep the original file?")
        self.format_file(file_path, original=keep_original)

    def format_file(self, file_path, original=False):
        try:
            with open(file_path, 'r') as file:
                original_code = file.read()

            formatted_code = autopep8.fix_code(original_code, options={'aggressive': 1})

            if original:
                base, ext = os.path.splitext(file_path)
                new_file_path = f"{base}_formatted{ext}"
                with open(new_file_path, 'w') as file:
                    file.write(formatted_code)
                self.output(f"Formatted and saved as new file: {os.path.basename(new_file_path)}")
            else:
                with open(file_path, 'w') as file:
                    file.write(formatted_code)
                self.output(f"Formatted: {os.path.basename(file_path)}")

        except Exception as e:
           mb.showerror("Error", f"An error occurred while formatting: {e}")

    def output(self, message):
        self.wtext.insert(tk.END, message + '\n')
        self.wtext.insert(tk.END)

