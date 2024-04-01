import tkinter as tk
from tkinter import ttk, Toplevel
import tkinter as tk
from tkinter import ttk
from tkinter.font import families

class FontBar:
    def __init__(self, parent,textwidget):
        self.parent = parent
        self.textwidget = textwidget
        self.top = tk.Toplevel(parent)

        self.frame = tk.Frame(self.top)
        self.frame.grid(row=0, column=0)
        self.toolbar = tk.Canvas(self.frame, width=40, height=15,bg="orange")
        self.toolbar.grid(row=0, column=0, sticky="ew")
        
        
        self.scrollbar = tk.Scrollbar(self.top)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.font_listbox = tk.Listbox(self.top, width=50, yscrollcommand=scrollbar.set)
        self.font_listbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.scrollbar.config(command=font_listbox.yview)
        self.fonts_list = list(font.families())
        self.fonts_list.sort()
        for f in fonts_list:
            self.font_listbox.insert(tk.END, f)
            self.example_label = tk.Label(self.top, text='Example Text', font=('Arial', 12))
            self.example_label.grid(row=1, column=0, padx=10, pady=20, columnspan=2)
            self.font_listbox.bind('<<ListboxSelect>>', update_font_example)

        
        self.font_size_var = tk.IntVar(value=12)
        self.font_size_combobox = ttk.Combobox(
        self.toolbar, textvariable=self.font_size_var, state="readonly",
            values=list(range(8, 80, 2)), width=10)
        self.font_size_combobox.grid(row=0, column=1, padx=5)
        self.font_size_combobox.bind("<<ComboboxSelected>>", self.change_font)


        
        self.font_size_combobox.grid(row=0, column=1, padx=5)
        self.font_size_combobox.bind("<<ComboboxSelected>>", self.change_font)

       
    def change_font(self, event=None):
        font_family = self.font_family_var.get()
        font_size = self.font_size_var.get()
        self.textwidget.configure(font=(font_family, font_size))

