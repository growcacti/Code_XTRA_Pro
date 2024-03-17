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
        
        self.font_family_var = tk.StringVar()
        self.font_family_combobox = ttk.Combobox(
            self.toolbar, textvariable=self.font_family_var, state="readonly",
            values=sorted(families()), width=30)
        self.font_family_combobox.grid(row=0, column=0, padx=5)
        self.font_family_combobox.set("Liberation Serif")
        self.font_family_combobox.bind("<<ComboboxSelected>>", self.change_font)

        self.font_size_var = tk.IntVar(value=12)
        self.font_size_combobox = ttk.Combobox(
            self.toolbar, textvariable=self.font_size_var, state="readonly",
            values=list(range(8, 80, 2)), width=10)
        self.font_size_combobox.grid(row=0, column=1, padx=5)
        self.font_size_combobox.bind("<<ComboboxSelected>>", self.change_font)

       
    def change_font(self, event=None):
        font_family = self.font_family_var.get()
        font_size = self.font_size_var.get()
        self.textwidget.configure(font=(font_family, font_size))

