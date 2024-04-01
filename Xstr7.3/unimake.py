import tkinter as tk
from tkinter import ttk, INSERT,END,font,Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from string import punctuation

class UnicodeListGeneratorApp:
    def __init__(self, parent):
        self.parent = parent
        listbox_font = font.Font(family="Helvetica", size=32)     
        # Create and place labels, entries, and button
        start_label = ttk.Label(self.parent, text="Start (hex):")
        start_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

        end_label = ttk.Label(self.parent, text="End (hex):")
        end_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.start_entry = ttk.Entry(self.parent, width=10)
        self.start_entry.grid(row=1, column=1, padx=10, pady=5)

        self.end_entry = ttk.Entry(self.parent, width=10)
        self.end_entry.grid(row=2, column=1, padx=10, pady=5)

        generate_button = ttk.Button(self.parent, text="Generate", command=self.generate_unicode)
        generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(self.parent, text="Save to File", command=self.save_to_file)
        save_button.grid(row=3, column=4)

        clear_button = ttk.Button(self.parent, text="Clear list", command=self.clear)
        clear_button.grid(row=3, column=6, pady=10)

        # Create and place listbox for output
        self.output_listbox = tk.Listbox(self.parent, width=20, height=15)
        self.output_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.output_listbox2 = tk.Listbox(self.parent, width=10, height=5, font=listbox_font)
        self.output_listbox2.grid(row=4, column=5, padx=10, pady=5)
        self.unitext = ScrolledText(
            self.parent,
            height=20,
            width=20,
            bg="white",
            bd=10)
        self.unitext.grid(row=4, column=7)
    def generate_unicode(self):
        start_hex = self.start_entry.get()
        end_hex = self.end_entry.get()

        # Convert hex strings to integers
        start_int = int(start_hex, 16)
        end_int = int(end_hex, 16)

        # Clear the listbox
        self.output_listbox.delete(0, tk.END)
        self.output_listbox2.delete(0, tk.END)

        # Add characters to the listbox
        for code_point in range(start_int, end_int + 1):
            char = chr(code_point)
            hex_value = f"{code_point:04X}"
            self.output_listbox.insert(tk.END, f"U+{hex_value}: {char}")
            self.output_listbox2.insert(tk.END, f"        {char}")
            self.unitext.insert(tk.END, f"        {char}")
            self.unitext.insert(tk.END, f"U+{hex_value}: {char}")
    def save_to_file(self):
        # Choose where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt"),
                                                             ("All files", "*.*")])
        if not file_path:  # if the user cancels the save
            return

        with open(file_path, 'w', encoding='utf-8') as file:
            for item in self.output_listbox.get(0, tk.END):
                file.write(item + ',' + '\n')

    def clear(self):
        self.output_listbox.delete(0, tk.END)
        

