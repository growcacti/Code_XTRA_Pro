import tkinter as tk
from tkinter import ttk
from tkinter.font import families

class FontBar:
    def __init__(self, parent, textwidget):
        self.parent = parent
        self.textwidget = textwidget
        self.top = tk.Toplevel(parent)
        self.font = ("Liberation Serif", 12)  # Default font
        self.frame = tk.Frame(self.top)
        self.frame.grid(row=0, column=0, sticky="ew")
        
        self.toolbar = tk.Canvas(self.frame, width=40, height=15, bg="orange")
        self.toolbar.grid(row=0, column=0, sticky="ew")
        
        # Scrollbar setup
        self.scrollbar = tk.Scrollbar(self.top)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Listbox for fonts
        self.font_listbox = tk.Listbox(self.top, width=50, yscrollcommand=self.scrollbar.set)
        self.font_listbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Configure scrollbar
        self.scrollbar.config(command=self.font_listbox.yview)
        
        # Insert font names into Listbox
        self.fonts_list = list(families())
        self.fonts_list.sort()
        for f in self.fonts_list:
            self.font_listbox.insert(tk.END, f)
        
        # Example label to display selected font
        self.example_label = tk.Label(self.top, text='Example Text', font=self.font)
        self.example_label.grid(row=1, column=0, padx=10, pady=20, columnspan=2)
        
        # Bind the Listbox selection event
        self.font_listbox.bind('<<ListboxSelect>>', self.update_font_example)
        
        # Font size selection
        self.font_size_var = tk.IntVar(value=12)
        self.font_size_combobox = ttk.Combobox(self.toolbar, textvariable=self.font_size_var, state="readonly", values=list(range(8, 80, 2)), width=10)
        self.font_size_combobox.grid(row=0, column=1, padx=5)
        self.font_size_combobox.bind("<<ComboboxSelected>>", self.change_font)

    def change_font(self, event=None):
        font_family = self.font_listbox.get(self.font_listbox.curselection())
        font_size = self.font_size_var.get()
        self.font = (font_family, font_size)
        self.textwidget.configure(self.font)
        self.update_font_example()

    def update_font_example(self, event=None):
        if not self.font_listbox.curselection():
            return  # Exit if nothing is selected
        selected_font = self.font_listbox.get(self.font_listbox.curselection())
        self.example_label.config(font=(selected_font, 12))
        self.example_label['text'] = f'This is "{selected_font}" font'
