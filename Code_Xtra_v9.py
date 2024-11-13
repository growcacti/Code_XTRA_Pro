import tkinter as tk
from tkinter.scrolledtext import ScrolledText 
from tkinter import ttk, INSERT, END, ANCHOR, font, Toplevel,simpledialog, colorchooser
from tkinter import Button, Frame, Entry, END, Canvas, Scrollbar
from tkinter.font import Font, families
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from datetime import datetime
from tkinter.font import Font, families
from string import punctuation
import subprocess
import threading
from collections import Counter
import re
import sys
import os
import runpy
import re
####User Modules#####

from txinfo2 import *
from compare2 import *
from unimake import *
from codefab import *
from py_dir_doc_helper import *
from filefnr import *
from remove_stuff import *
from findreplace import *
from listmaker import *
from fontbar import *
from txt2list import *
from pyrun import *
from showcolors import *
from synhigh2 import *


class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.bar_frm = tk.Frame(self.parent)
        self.bar_frm.grid(row=0, column=0, sticky="ew")
        self.parent.columnconfigure(0, weight=1)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.parent.rowconfigure(1, weight=1)
        self.frm0 = ttk.Frame(self.notebook)
        self.frm1 = ttk.Frame(self.notebook)
        self.frm2 = ttk.Frame(self.notebook)
        self.highlight_debounce_timer = None
        self.notebook.add(self.frm0, text="Main")
        self.notebook.add(self.frm1, text="Py Module Doc & Dir Helper")
        self.notebook.add(self.frm2, text="Sub")
        self.txtfrm = tk.Frame(self.frm0)
        self.txtfrm.grid(row=0, column=2, sticky="nsew")
        self.frm0.columnconfigure(2, weight=3)
        self.tx = ScrolledText(self.txtfrm, bg="white", bd=12)
        self.tx.grid(row=0, column=1, sticky="nsew")
        self.txtfrm.rowconfigure(0, weight=1)
        self.subnote = ttk.Notebook(self.frm2)
        self.subnote.grid(row=2, column=1)
        self.viewfrm = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm, text="0")
        self.txt0= ScrolledText(self.viewfrm, bg="white", bd=12)
        self.txt0.grid(row=0, column=1, sticky="nsew")
        self.keywords = {'keyword': r'\b(import|as|pass|return|def)\b',
                         'string': r'".*?"|\'.*?\'' }
    

        self.py_viewer = PyDDViewer(self.frm1)

        self.viewfrm1 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm1, text="1")
        self.txt1= ScrolledText(self.viewfrm1,height=40,width=120, bg="lavender", bd=12)
        self.txt1.grid(row=0, column=1, sticky="nsew")

        self.viewfrm2 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm2, text="2")
        self.txt2= ScrolledText(self.viewfrm2,height=40,width=120,bg="white", bd=12)
        self.txt2.grid(row=0, column=1, sticky="nsew")

        self.viewfrm3 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm3, text="3")
        self.txt3= ScrolledText(self.viewfrm3,height=40,width=120, bg="seashell", bd=12)
        self.txt3.grid(row=0, column=1, sticky="nsew")

        self.viewfrm4 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm4, text="4")
        self.txt4= ScrolledText(self.viewfrm4,height=40,width=120, bg="alice blue", bd=12)
        self.txt4.grid(row=0, column=1, sticky="nsew")

        self.viewfrm5 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm5, text="5")
        self.txt5= ScrolledText(self.viewfrm5,height=40,width=120, bg="azure", bd=12)
        self.txt5.grid(row=0, column=1, sticky="nsew")

        self.viewfrm6 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm6, text="6")
        self.txt6= ScrolledText(self.viewfrm6,height=40,width=120, bg="oldlace", bd=12)
        self.txt6.grid(row=0, column=1, sticky="nsew")

        self.viewfrm7 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm7, text="7")
        self.txt7= ScrolledText(self.viewfrm7,height=40,width=120, bg="whitesmoke", bd=12)
        self.txt7.grid(row=0, column=1, sticky="nsew")


        self.viewfrm8 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm8, text="8")
        self.txt8= ScrolledText(self.viewfrm8,height=40,width=120, bg="snow", bd=12)
        self.txt8.grid(row=0, column=1, sticky="nsew")

        self.viewfrm9 = ttk.Frame(self.subnote)
        self.subnote.add(self.viewfrm9, text="9")
        self.txt9= ScrolledText(self.viewfrm9,height=40,width=120, bg="white", bd=12)
        self.txt9.grid(row=0, column=1, sticky="nsew")

       
        self.path = os.getcwd()
        self.tree_frame = tk.Frame(self.frm0)
        self.tree_frame.grid(row=0, column=1, sticky="nsew")
       
        # Update columns to include file size and date added
        self.columns = ("filename", "size", "modified")
        self.treeview = ttk.Treeview(
            self.tree_frame,
            columns=self.columns,
            show="headings")
        self.treeview.grid(row=0, column=1, sticky="nsew")
        self.frm0.columnconfigure(1, weight=1)

        # Configure column headings and widths
        self.treeview.heading(
            "filename",
            text="Filename",
            command=lambda: self.sort_treeview(
                "filename",
                False))
        self.treeview.column("filename", width=200)
        self.treeview.heading(
            "size",
            text="Size",
            command=lambda: self.sort_treeview(
                "size",
                False))
        self.treeview.column("size", width=100)
        self.treeview.heading(
            "modified",
            text="Modified",
            command=lambda: self.sort_treeview(
                "modified",
                False))
        self.treeview.column("modified", width=150)

        # Scroltreeviewar for the Treeview
        self.tree_scr = tk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.treeview.yview)
        self.tree_scr.grid(row=0, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=self.tree_scr.set)
        self.treeviewfrm = tk.Frame(self.frm1, width=5, height=30)
        self.treeviewfrm.grid(row=0, column=1)

        self.treeview.grid(row=0, column=2)
        self.treeview.focus()
        for col in self.columns:
            self.treeview.heading(col, text=col.capitalize(),
                                  command=lambda _col=col: self.sort_by(_col, False))

       # Buttons frame
        self.fr_buttons = tk.Frame(self.frm0)
        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.frm1.columnconfigure(0, weight=1)
  
        self.btn_1 = tk.Button(
            self.fr_buttons,
            text="Change Dir",
            bd=3,
            command=self.newdirlist)
        self.btn_1.grid(row=2, column=0)                          
        self.btn_2 = tk.Button(self.fr_buttons,text="Recursive Dir",bd=2, command=self.recursive_new_list)
        self.btn_2.grid(row=3, column=0)       

        self.sbox = tk.Spinbox(self.fr_buttons, from_=1, to=12)
        self.sbox.grid(row=5, column=0, padx=10, pady=10)

       
        self.btn = tk.Button(
            self.fr_buttons,
            text="Send to txt index",
            bd=6,
            command=lambda : self.ggtxt())
        self.btn.grid(row=6, column=0)
        
        self.frm2 = ttk.Frame(self.notebook, width=60, height=50)
        self.notebook.add(self.frm2, text="Text")
        self.text1 = ScrolledText(
            self.frm2,
            height=30,
            width=120,
            bg="white",
            bd=10)
        self.text1.grid(row=4, column=1, sticky="nsew")
        self.text1.delete("1.0", "end-1c")
    

        self.frm3 = ttk.Frame(self.notebook, width=50, height=44)
        self.notebook.add(self.frm3, text="Editor")
        self.text2 = ScrolledText(
            self.frm3,
            height=40,
            width=120,
            bg="white",
            bd=10)
        self.text2.grid(row=5, column=1, sticky="nsew")
        self.text2.delete("1.0", "end-1c")
        self.frm4 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm4, text="Compare Text")
        self.textcompare = TextFileComparator(self.frm4)
        self.textcompare.run()
        self.frm5 = ttk.Frame(self.notebook, width=50, height=600)
        self.notebook.add(self.frm5, text="Unicode_Generator")
        self.uni = UnicodeListGeneratorApp(self.frm5)
        self.frm6 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm6, text="Codefab")
        self.code = CodeEditorApp(self.frm6)
        self.frm7 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm7, text="Colors Info")
        colortest = ColorTester(self.frm7)
        
        self.frm8 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm8, text="Run A Py PRG")
        
        self.txt = ScrolledText(
            self.frm8,
            height=30,
            width=40,
            bg="white",
            bd=10)
        self.txt.grid(row=2, column=2)
        self.runbtn1 = tk.Button(
            self.frm8,
            text="Select Python File Run", command=lambda : self.pyrun(1))
        self.runbtn1.grid(row=5, column=5)

        self.runbtn2 = tk.Button(
            self.frm8,
            text="Using Subprocess Run", command=lambda : self.pyrun(2))
        self.runbtn2.grid(row=5, column=6)
        self.frm9 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm9, text="9")
        self.text3 = ScrolledText(
            self.frm9,
            height=40,
            width=100,
            bg="white",
            bd=10)
        self.text3.grid(row=5, column=1, sticky="nsew")
       
    
        
        self.frm10 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm10, text="create file and directories")
        tk.Label(self.frm10, text="Enter file names (comma separated):").grid(row=0, column=0, sticky="w")
        self.file_entry = Entry(self.frm10, width=50)
        self.file_entry.grid(row=0, column=1)

        tk.Label(self.frm10, text="Enter directory names (comma separated):").grid(row=1, column=0, sticky="w")
        self.dir_entry = Entry(self.frm10, width=50)
        self.dir_entry.grid(row=1, column=1)

        self.btn = Button(self.frm10, text="Create", command=self.create_files_directories).grid(row=2, column=0, columnspan=2)
        self.feedback_text = ScrolledText(
                    self.frm10,
                    height=30,
                    width=120,
                    bg="white",
                    bd=10)


        self.feedback_text.grid(row=3, column=0, columnspan=2, sticky="nsew")
       
        
        self.frm11 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm11, text="MultiFile Find&Replace")
        self.filefindreplace = FindReplaceApp(self.frm11)
        self.info1 = TextWidgetInfo(self.frm0, self.tx)
        self.info2 = TextWidgetInfo(self.frm2, self.text1)
        self.info3 = TextWidgetInfo(self.frm3, self.text2)
        self.info4 = TextWidgetInfo(self.viewfrm, self.txt0)
        self.info5 = TextWidgetInfo(self.viewfrm1, self.txt1)
        self.info6 = TextWidgetInfo(self.viewfrm2, self.txt2)
        self.info7 = TextWidgetInfo(self.viewfrm3, self.txt3)
        self.info8 = TextWidgetInfo(self.viewfrm4, self.txt4)
        self.info9 = TextWidgetInfo(self.viewfrm5, self.txt5)
        self.info10 = TextWidgetInfo(self.viewfrm6, self.txt6)
        self.info11 = TextWidgetInfo(self.viewfrm7, self.txt7)
        self.info12 = TextWidgetInfo(self.viewfrm8, self.txt8)
        self.info13 = TextWidgetInfo(self.viewfrm9, self.txt9)
        self.textwidgets = [self.tx, self.text1,self.txt, self.text2,
                            self.txt0,self.txt1,self.txt2,self.txt3,self.txt4,
                            self.txt5,self.txt6,self.txt7,self.txt8,self.txt9]
        self.frm12 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm12, text="Rmv_Line #")
        self.rmv = remove_add(self.frm12)
        self.frm13 = ttk.Frame(self.notebook, width=50, height=60)
        self.frm14 = ttk.Frame(self.notebook, width=50, height=60)

        self.notebook.add(self.frm13, text="Py listmaker edit")
        self.notebook.add(self.frm14, text="Text2List")
        self.listmake = ListEditorApp(self.frm13)
        self.text2list= TextToListConverter(self.frm14)
        self.frm15 = ttk.Frame(self.notebook)
        self.notebook.add(self.frm15, text="other text adjust")
        self.insertentry=tk.Entry(self.frm15, bd=8, bg="seashell2")
        self.insertentry.grid(row=4, column=1)

        self.notebook.bind("<<NotebookTabChanged>>", self.ontab_notebook)
        self.subnote.bind("<<NotebookTabChanged>>", self.ontab_notebook)                                    
        self.menubar = tk.Menu(self.parent, tearoff=False)
        self.keywords = ['def', 'class', 'if', 'else', 'try', 'except', 'True', 'False', 'None', 'as', 'assert', 'async', 'await', 'break', 'continue', 'del', 'elif', 'finally', 'for', 'from', 'global', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'while', 'with', 'yield']

        self.file_menu = tk.Menu(self.menubar)
        self.edit_menu = tk.Menu(self.menubar)
        self.view_menu = tk.Menu(self.menubar)
        self.cursor_menu = tk.Menu(self.menubar)
        self.format_menu = tk.Menu(self.menubar)
       
 
  

      
        self.listing()
     
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="New", underline=1, command=lambda: self.clear(self.textwidget)
        )
        self.file_menu.add_command(
            label="Open", underline=1, command=lambda: self.open_file()
        )
        self.file_menu.add_command(
            label="Save", underline=1, command=lambda: self.save_file()
        )
        self.file_menu.add_command(
            label="readlines", underline=1, command=lambda: self.readlines()
        )
            
###################
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Replace After Pattern...", command=self.replace_after_pattern)
        self.edit_menu.add_command(label="Replace Before Pattern...", command=self.replace_before_pattern)
        self.edit_menu.add_command(label="Regex Substitute...", command=self.regex_substitute)
        self.edit_menu.add_command(
            label="Select All",
            accelerator="Ctrl+A",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<SelectAll>>"),
        )
        self.edit_menu.add_command(
            label="Cut",
            accelerator="Ctrl+X",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Cut>>"),
        )
        self.edit_menu.add_command(
            label="Copy",
            accelerator="Ctrl+C",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Copy>>"),
        )
        self.edit_menu.add_command(
            label="Paste",
            accelerator="Ctrl+V",
            compound="left",
            underline=0,
            command=lambda: self.textwidget.event_generate("<<Paste>>"),
        )
        self.edit_menu.add_command(
            label="---",
            compound="left",
            underline=0,
            command=None
        )
        self.edit_menu.add_command(
            label="---",
            accelerator="Ctrl+Y",
            compound="left",
            underline=0,
            command=None,
        )       

        self.edit_menu.add_command(
            label="Find",
            accelerator="Ctrl+F",
            compound="left",
            underline=0,
            command=lambda: self.findreplace(),
        )
        self.edit_menu.add_command(
            label="Replace",
            accelerator="Ctrl+R",
            compound="left",
            underline=0,
            command=lambda: self.findreplace(),
        )
        self.edit_menu.add_command(
            label="cleartags",
            accelerator="Ctrl+G",
            compound="left",
            underline=0,
            command=lambda: self.cleartags(),
        )


####################################################################
        self.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(
            label="----", compound="left", underline=0, command=None
        )
        self.view_menu.add_command(
            label="Backgrounbd Color",
            compound="left",
            underline=0,
            command=lambda: self.change_bg(),
        )
        self.view_menu.add_command(
            label="Foreground Color",
            compound="left",
            underline=0,
            command=lambda: self.change_fg(),
        )
        self.view_menu.add_command(
            label="Highlight Line",
            compound="left",
            underline=0,
            command=lambda: self.highlight_line(),
        )
        self.view_menu.add_command(
            label="Foreground Color",
            compound="left",
            underline=0,
            command=lambda: self.change_fg(),
        )

        self.view_menu.add_command(label="Size & Type", command=lambda : self.font(self.textwidget))
        self.view_menu.add_command(label="Font Color", command=self.change_font_color)
        self.view_menu.add_command(label="Bold", command=self.toggle_bold)
        self.view_menu.add_command(label="Italic", command=self.toggle_italic)
        self.view_menu.add_command(label="Underline", command=self.toggle_underline)
        self.view_menu.add_command(label="Left", command=self.align_left)
        self.view_menu.add_command(label="Center", command=self.align_center)
        self.view_menu.add_command(label="Right", command=self.align_right)
       

##########################################################################
        self.add_cascade(label="Cursor", menu=self.cursor_menu)
        self.cursor_menu.add_command(
            label="Ahead_four_chars",
            underline=1,
            command=lambda: self.ahead_four_chars(),
        )
        self.cursor_menu.add_command(
            label="Highlight_line", underline=1, command=lambda: self.highlight_line()
        )
        self.cursor_menu.add_command(
            label="Back_four_chars", underline=1, command=lambda: self.back_four_chars()
        )
        self.cursor_menu.add_command(
            label="Down_three_lines",
            underline=1,
            command=lambda: self.down_three_lines(),)

        self.cursor_menu.add_command(
            label="Down_six_lines",
            underline=1,
            command=lambda: self.down_six_lines(),
        )

        self.cursor_menu.add_command(
            label="Downlines", underline=1, command=lambda: self.downlines()
        )
        self.cursor_menu.add_command(
            label="Tag alternating",
            underline=1,
            command=self.tag_alternating,
        )

        self.cursor_menu.add_command(
            label="Cursor to top of page",
            underline=1,
            command=self.cursor_to_top,)
        self.cursor_menu.add_command(
            label="Cursor to bottom",
            underline=1,
            command=self.cursor_to_bottom,
        )
        self.cursor_menu.add_command(
            label="-----",
            underline=1,
            command=None,
        )

###########################################################################
        self.add_cascade(label="Format", menu=self.format_menu)

        self.format_menu.add_command(
            label="Indent",
            accelerator="Ctrl+[",
            compound="left",
            underline=0,
            command=lambda: self.indent(self.textwidget),
        )
        self.format_menu.add_command(
            label="Dedent",
            accelerator="Ctrl+[",
            compound="left",
            underline=0,
            command=lambda: self.dedent(self.textwidget),
        )
        self.format_menu.add_command(
            label="Insert Self make OOP",
            compound="left",
            underline=0,
            command=lambda: self.insert_selfs(self.textwidget),
        )
        self.format_menu.add_command(
            label=" highlight_line",
            compound="left",
            underline=0,
            command=self.highlight_line,
        )
        self.format_menu.add_command(
            label="Change funct to Method",
            compound="left",
            underline=0,
            command=lambda: self.insert_self_in_parentheses(self.textwidget),
        )
        self.format_menu.add_command(
            label="------------",
            compound="left",
            underline=0,
            command=None,
        )
        self.format_menu.add_command(
            label="Remove ALL Comments #",
            compound="left",
            underline=0,
            command=self.remove_comments
        )
        self.format_menu.add_command(
            label=" pygameaspg",
            compound="left",
            underline=0,
            command=self.pygameaspg
        )

       
        
        self.format_menu.add_command(
            label="--------------",
            compound="left",
            underline=0,
            command=None,
        )
        self.format_menu.add_command(
            label="Insert at Cursor",
            compound="left",
            underline=0,
            command=None,
        )
        self.format_menu.add_command(
            label="------",
            compound="left",
            underline=0,
            command=None)

        self.format_menu.add_command(
            label="CamelCase to snake_case",
            compound="left",
            underline=0,
            command=self.convert_to_snake_case
        )
        self.format_menu.add_command(
            label="to lowercase",
            compound="left",
            underline=0,
            command=self.to_lowercase)
        self.format_menu.add_command(
            label="to uppercase",
            compound="left",
            underline=0,
            command=self.to_uppercase)




        self.format_menu.add_command(
            label="to captilization",
            compound="left",
            underline=0,
            command=self.to_cap)
        self.format_menu.add_command(
            label="to titlecase",
            compound="left",
            underline=0,
            command=self.to_titlecase)
        self.format_menu.add_command(
            label="to swapcase",
            compound="left",
            underline=0,
            command=self.to_swapcase)    
        self.format_menu.add_command(
            label="Remove Line Containing",
            compound="left",
            underline=0,
            command=self.remove_lines_containing
            )

        self.format_menu.add_command(
            label="------------",
            compound="left",
            underline=0,
            command=None,
        )

        
        self.format_menu.add_command(
            label="Create a list like output",
            compound="left",
            underline=0,
            command=self.read_file_and_remove_duplicates,
            )
        self.format_menu.add_command(
            label="Syntax HighLighting",
            compound="left",
            underline=0,
            command=self.syntax,
        )
               

        
        self.binding()
        self.makedirlist()
        self.update_info()
    
    ####################METHODS ###OF###THIS####CLASS####################################

    def binding(self):
        self.treeview.bind("<<TreeviewSelect>>", self.showcontent)
        self.treeview.bind("<Double-Button-1>", self.on_double_click)
       
 
    def syntax(self):
       
        syn = SyntaxHighlite(self.ontab_notebook())
        syn.highlight_syntax()
        
    def get_pattern_and_replacement(self, prompt):
        pattern = simpledialog.askstring("Input", f"Enter pattern {prompt}:")
        if not pattern:
            return None, None
        replacement = simpledialog.askstring("Input", "Enter replacement text:")
        return pattern, replacement
    
    def replace_after_pattern(self):
        pattern, replacement = self.get_pattern_and_replacement("to replace after (inclusive)")
        if pattern is not None:
            modified_text = re.sub(f"{pattern}.*", f"{pattern}{replacement}",self.textwidget.get("1.0", tk.END))
            self.textwidget.delete("1.0", tk.END)
            self.textwidget.insert("1.0", modified_text)
    
    def replace_before_pattern(self):
        pattern, replacement = self.get_pattern_and_replacement("to replace before (exclusive)")
        if pattern is not None:
            modified_text = re.sub(f".*{pattern}", f"{replacement}{pattern}",self.textwidget.get("1.0", tk.END), count=1)
            self.textwidget.delete("1.0", tk.END)
            self.textwidget.insert("1.0", modified_text)
    
    def regex_substitute(self):
        pattern, replacement = self.get_pattern_and_replacement("for regex substitute")
        if pattern is not None:
            modified_text = re.sub(pattern, replacement,self.textwidget.get("1.0", tk.END))
            self.textwidget.delete("1.0", tk.END)
            self.textwidget.insert("1.0", modified_text)
   

    def pyrun(self,sel):
        if sel == 1:
            run = Pyscript_Run(self.txt)
            run.run_python_file()
        if sel == 2:
            run2 = Pyscript_Run(self.txt)
            run2.run_subprocess()
       
    def change_font_color(self, event=None):
        try:
            (rgb, hx) = tk.colorchooser.askcolor()
            self.textwidget.tag_add("color", "sel.first", "sel.last")
            self.textwidget.tag_configure("color", foreground=hx)
            # self.textwidget.tag_configure(rgb, foreground=hx)
        except tk.TclError as ex:
            print(ex)

        
    def toggle_bold(self):
        try:
            self.current_tags = self.textwidget.tag_names("sel.first")
            if "bold" in self.current_tags:
                self.textwidget.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.textwidget.tag_add("bold", "sel.first", "sel.last")
                bold_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
                bold_font.configure(weight="bold")
                self.textwidget.tag_configure("bold", font=bold_font)
        except tk.TclError as ex:
            print(ex)

    

    def toggle_italic(self):
        try:
            self.current_tags = self.textwidget.tag_names("sel.first")
            if "italic" in self.current_tags:
                self.textwidget.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.textwidget.tag_add("italic", "sel.first", "sel.last")
                italic_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
                italic_font.configure(slant="italic")
                self.textwidget.tag_configure("italic", font=italic_font)
        except tk.TclError as ex:
            print(ex)


    def toggle_underline(self):
        try:
            self.current_tags = self.textwidget.tag_names("sel.first")
            if "underline" in self.current_tags:
                self.textwidget.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.textwidget.tag_add("underline", "sel.first", "sel.last")
                underline_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
                underline_font.configure(underline=1)
                self.textwidget.tag_configure("underline", font=underline_font)
        except tk.TclError as ex:
            print(ex)

    def align_left(self, event=None):
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("left", justify=tk.LEFT)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "left")

    def align_center(self, event=None):
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("center", justify=tk.CENTER)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "center")


    def align_right(self, event=None):
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("right", justify=tk.RIGHT)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "right")

    def changeall_bold(self):
        self.textwidget.tag_add("bold", "1.0", "end")
        bold_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
        bold_font.configure(weight="bold")
        self.textwidget.tag_configure("bold", font=bold_font)

    def changeall_italic(self):
        self.textwidget.tag_add("italic", "1.0", "end")
        italic_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
        italic_font.configure(slant="italic")
        self.textwidget.tag_configure("italic", font=italic_font)

    def changeall_underline(self):
        self.textwidget.tag_add("underline", "1.0", "end")
        underline_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
        underline_font.configure(underline=1)
        self.textwidget.tag_configure("underline", font=underline_font)       
    def add_file_to_treeview(self, root, file):
       
        item_path = os.path.join(root, file)  # Full path to the item
        file_size = os.path.getsize(item_path)  # Get file size
        modified_timestamp = os.path.getmtime(item_path)  # Get last modified timestamp
        modified_date = datetime.fromtimestamp(modified_timestamp).strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp

        # Insert the file information into the Treeview
        self.treeview.insert('', 'end', values=(item_path, file_size, modified_date))
     
   
    def sort_by(self, col, descending):
        """Sort Treeview content by a column."""
        self.listing()
        # Retrieve data from Treeview as a list of tuples
        data_list = [(self.treeview.item(iid, 'values'), iid)
                     for iid in self.treeview.get_children('')]

        # Sort the list in either ascending or descending order
        # Adjust the key=lambda part based on the data type of the column
        data_list.sort(
            key=lambda x: x[0][self.columns.index(col)], reverse=descending)

        # Rearrange items in sorted positions
        for index, item in enumerate(data_list):
            self.treeview.move(item[1], '', index)

        # Reverse the sorting order for the next sort operation
        self.treeview.heading(
            col, command=lambda: self.sort_by(
                col, not descending))

    def on_double_click(self, event):
        # This method will be triggered on a double-click event on a Treeview
        # item
        selected_item = self.treeview.selection()
        if selected_item:
            self.showcontent()
            print(
                f"Double-clicked on: {self.treeview.item(selected_item[0])['values']}")

      
   

    def makedirlist(self):
        self.path = os.getcwd()
        self.listing()


    def recursive_new_list(self):
        self.path = askdirectory()
        if self.path:  # Check if a directory was selected
            os.chdir(self.path)
        for root, dirs, files in os.walk(self.path):
                for file in files:
                        if file.endswith((".py", ".txt")):
                            self.add_file_to_treeview(root, file)    

                          

   

    def newdirlist(self):
        self.path = askdirectory()
        if self.path:  # Check if a directory was selected
            os.chdir(self.path)
         
            self.listing()

    def listing(self, event=None):
        self.flist = os.listdir(self.path)
        self.treeview.delete(*self.treeview.get_children())  # Clear the Treeview
        for item in self.flist:
            if item.endswith((".py", ".txt")):
                file_size = os.path.getsize(item)  # Example for file size
                modified_timestamp = os.path.getmtime(item)
                modified_date = datetime.fromtimestamp(modified_timestamp).strftime('%Y-%m-%d %H:%M:%S')  # Formatted date

                # Inserting into the Treeview
                self.treeview.insert('', 'end', values=(item, file_size, modified_date))



               

    def showcontent(self, event=None):
        selected_item = self.treeview.selection()
        if selected_item:
            file_name = self.treeview.item(selected_item[0])['values'][0]
            file_path = os.path.join(self.path, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as file_content:
                        content = file_content.read()
                        self.tx.delete("1.0", tk.END)
                        self.tx.insert(tk.END, content)
                except Exception as e:
                    print(f"Error opening file: {e}")
            else:
                print("Selected file does not exist.")

    def update_info(self):
        # Update every textwidget associated with TextWidgeInfo class
        self.info1.update_info()
        self.info2.update_info()
        self.info3.update_info()
        self.info4.update_info()
        self.info5.update_info()
        self.info6.update_info()
        self.info7.update_info()
        self.info8.update_info()
        self.info9.update_info()
        self.info10.update_info()
        self.info11.update_info()
        self.info12.update_info()
        self.info13.update_info()

    def sort_treeview(self, col, reverse):
        # Fetching all children of the Treeview
        items = [(self.treeview.item(iid, 'values'), iid)
                 for iid in self.treeview.get_children('')]

        # Sort the items based on the specified column
        items.sort(key=lambda k: k[0][col], reverse=reverse)

        # Rearrange items in the Treeview
        for index, (values, iid) in enumerate(items):
            self.treeview.move(iid, '', index)

        # Reverse sort next time
        self.treeview.heading(
            col, command=lambda: self.sort_treeview(
                col, not reverse))

    def ggtxt(self):
        gettxt= self.tx.get("1.0", tk.END)
        
        if self.sbox.get() == "1":
            self.txt1.delete("1.0", tk.END)
            self.txt1.insert(tk.END, gettxt)
        elif self.sbox.get() == "2":
            self.txt2.delete("1.0", tk.END)
            self.txt2.insert(tk.END, gettxt)                        
        elif self.sbox.get() == "3":
            self.txt3.delete("1.0", tk.END)
            self.txt3.insert(tk.END, gettxt)
        elif self.sbox.get() == "4":
            self.txt4.delete("1.0", tk.END)
            self.txt4.insert(tk.END, gettxt)                        
        elif self.sbox.get() == "5":
            self.txt5.delete("1.0", tk.END)
            self.txt5.insert(tk.END, gettxt)
        elif self.sbox.get() == "6":
            self.txt6.delete("1.0", tk.END)
            self.txt6.insert(tk.END, gettxt)                        
        elif self.sbox.get() == "7":
            self.txt7.delete("1.0", tk.END)
            self.txt7.insert(tk.END, gettxt)
        elif self.sbox.get() == "8":
            self.txt8.delete("1.0", tk.END)
            self.txt8.insert(tk.END, gettxt)
        elif self.sbox.get() == "9":
            self.txt8.delete("1.0", tk.END)
            self.txt8.insert(tk.END, gettxt)
        elif self.sbox.get() == "10":
            self.txt0.delete("1.0", tk.END)
            self.txt0.insert(tk.END, gettxt)
        elif self.sbox.get() == "11":
            self.text1.delete("1.0", tk.END)
            self.text1.insert(tk.END, gettxt)
        elif self.sbox.get() == "12":
            self.text2.delete("1.0", tk.END)
            self.text2.insert(tk.END, gettxt)

    def font(self,textwidget):
        fontbar = FontBar(self.parent,self.textwidget)
    def ontab_notebook(self,event=None):
        self.selected_index = self.notebook.index(self.notebook.select())
        self.textwidget = self.tx
        if self.selected_index == 0:
            self.textwidget = self.tx
        elif self.selected_index == 1:
            self.textwidget = self.py_viewer.textwidget
        elif self.selected_index == 2:
            self.textwidget = self.txt1
        elif self.selected_index == 3:
            self.textwidget = self.text1
        elif self.selected_index == 4:
            self.textwidget = self.text2
        elif self.selected_index == 5:
            self.textwidget = self.textcompare.text1
        elif self.selected_index == 6:
            self.textwidget = self.uni.unitext
        elif self.selected_index == 7:
            self.textwidget = self.code.textwidget
        elif self.selected_index == 8:
            self.textwidget = self.txt
        elif self.selected_index == 9:
            self.textwidget = self.txt
        elif self.selected_index == 10:
            self.textwidget = self.text3
        elif self.selected_index == 11:
            self.textwidget = None
        print(self.selected_index)
      
        self.selected_index2 = self.subnote.index(self.subnote.select())

        if self.selected_index2 == 0:
            self.textwidget = self.tx
        elif self.selected_index2  == 1:
            self.textwidget = self.txt1
        elif self.selected_index2  == 2:
            self.textwidget = self.txt2
        elif self.selected_index2  == 3:
            self.textwidget = self.txt3
        elif self.selected_index2  == 4:
            self.textwidget = self.txt4
        elif self.selected_index2  == 5:
            self.textwidget = self.txt5
        elif self.selected_index  == 6:
            self.textwidget = self.txt6
        elif self.selected_index2  == 7:
            self.textwidget = self.txt7
        elif self.selected_index2  == 8:
            self.textwidget = self.txt8
        elif self.selected_index2  == 9:
            self.textwidget = self.txt9
        print(self.selected_index2)    
        

        return self.textwidget    
    def create_files_directories(self):
        self.feedback_text.delete('1.0', END)
        filenames = self.file_entry.get().split(',')
        dirnames = self.dir_entry.get().split(',')

        for name in filenames:
            if name.strip():  # Ensure the name is not empty
                try:
                    with open(name.strip(), 'w') as f:
                        pass  # Just create the file if it doesn't exist
                    self.feedback_text.insert(END, f"File created: {name.strip()}\n")
                except Exception as e:
                    self.feedback_text.insert(END, f"Failed to create file {name.strip()}: {e}\n")

        for name in dirnames:
            if name.strip():  # Ensure the name is not empty
                try:
                    os.makedirs(name.strip(), exist_ok=True)
                    self.feedback_text.insert(END, f"Directory created: {name.strip()}\n")
                except Exception as e:
                    self.feedback_text.insert(END, f"Failed to create directory {name.strip()}: {e}\n")

       
    def sort_treeview(self):
        # Retrieve and sort the treeview items
        items = sorted(self.treeview.get(0, tk.END))

        # Update the treeview with sorted items
        self.treeview.delete(0, tk.END)  # Clear current items
        for item in items:
            self.treeview.insert(tk.END, item)

    def cursor_to_top(self):
        self.textwidget.mark_set("insert", "1.0")
        self.textwidget.see("insert")

    def cursor_to_bottom(self):
        self.textwidget.mark_set("insert", "end-1c")
        self.textwidget.see("insert")

    def cleartags(self):
        self.textwidget.tag_config(
            "found", foreground="black", background="white")

    def select_all(self, event=None):
        self.textwidget.tag_add("sel", "1.0", tk.END)
        return "break"

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.textwidget.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection="CLIPBOARD")
        self.insert("insert", text)

    def quit(self):
        sys.exit(0)

    def clear(self, textwidget):
        self.textwidget = textwidget
        self.textwidget.delete("1.0", tk.END)

    def cleare1(self):
        self.e1.delete(0, END)

    def change_bg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.textwidget.config(bg=hexstr)

    def change_fg(self):
        (triple, hexstr) = askcolor()

        if hexstr:
            self.textwidget.config(fg=hexstr)

    def command(self):
        pass

    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[
                ("Python Scripts", "*.py"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ]
        )
        if not filepath:
            return
        self.textwidget.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.textwidget.insert(tk.END, text)
            return filepath

    def save_file(self):
        filepath = asksaveasfilename(defaultextension=".py",
                                     filetypes=[("All Files", "*.*")],
                                     )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.textwidget.get(1.0, tk.END)
            output_file.write(text)
            return filepath

    def exit_application(self):
        """ Method to exit application """
        self.parent.destroy()

        sys.exit()

    def readlines(self):
        filepath = askopenfilename(filetypes=[("All Files", "*.*")])
        if not filepath:
            return
        self.textwidget.delete("1.0", tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.readlines()
  
    def findreplace(self):
        fnr = Find_Replace(self.parent,self.textwidget)
        
    def toggle_highlight(self, event=None):
        val = hltln.get()

        undo_highlight() if not val else highlight_line()

    def undo_highlight(self):
        self.self.textwidget.tag_remove("active_line", "1.0", tk.END)

    def output(self, message):
        self.textwidget.insert(tk.END, message + '\n')
        self.textwidget.insert(tk.END)

    def highlight_line(self, event=None):
        start = str(self.textwidget.index(tk.INSERT)) + " linestart"
        end = str(self.textwidget.index(tk.INSERT)) + " lineend"
        self.textwidget.tag_add("sel", start, end)

        return "break"

    def highlight_word(self, event=None):
        word_pos = str(self.textwidget.index(tk.INSERT))
        start = word_pos + " wordstart"
        end = word_pos + " wordend"
        self.textwidget.tag_add("sel", start, end)

        return "break"

    def down_six_lines(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+6l"
        self.textwidget.mark_set(tk.INSERT, new_position)

        return "break"
    def convert_to_snake_case(self):
        text = self.textwidget.get("1.0", tk.END)
        # Regular expression to identify camelCase words
        snake_case_text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", snake_case_text)  # Insert the modified text
    def remove_after(self):
        delimiter = simpledialog.askstring("Input", "Enter the delimiter or pattern:")
        use_regex = simpledialog.askstring("Input", "Use regex? (yes/no):")
        if delimiter:
            current_text = self.textwidget.get("1.0", tk.END)
            if use_regex.lower() == 'yes':
                pattern = re.escape(delimiter) + ".*"
                modified_text = re.sub(pattern, '', current_text, flags=re.DOTALL)
            else:
                modified_text = current_text.split(delimiter, 1)[0]
            self.textwidget.delete("1.0", tk.END)
            self.textwidget.insert("1.0", modified_text)

    def to_lowercase(self):
        text = self.textwidget.get("1.0", tk.END)
        # Simply convert the entire text to lowercase
        lower_case_text = text.lower()
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", lower_case_text)  # Insert the modified text



    def to_uppercase(self):
        text = self.textwidget.get("1.0", tk.END)
        # Simply convert the entire text to lowercase
        upper_case_text = text.upper()
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", upper_case_text)  # Insert the modified text



    def to_titlecase(self):
        text = self.textwidget.get("1.0", tk.END)
        # Simply convert the entire text to lowercase
        title_case_text = text.title()
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", title_case_text)  # Insert the modified text

    def to_cap(self):
        text = self.textwidget.get("1.0", tk.END)
        # Simply convert the entire text to lowercase
        cap_case_text = text.capitalize()
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", cap_case_text)  # Insert the modified text



    def to_swapcase(self):
        text = self.textwidget.get("1.0", tk.END)
        # Simply convert the entire text to lowercase
        swap_case_text = text.swapcase()
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", swap_case_text)  # Insert the modified text






    def remove_lines_containing(self):
        pattern = tk.simpledialog.askstring("Input", "Enter word/characters to remove lines containing:")
        if pattern is None:  # Cancel was pressed
            return
        text = self.textwidget.get("1.0", tk.END)
        lines = text.splitlines()
        # Keep lines that don't contain the pattern
        filtered_lines = [line for line in lines if not re.search(pattern, line, re.IGNORECASE)]
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", "\n".join(filtered_lines))  # Insert the filtered text
    def remove_comments(self):

        total_lines = int(self.textwidget.index('end-1c').split('.')[0])
        for line_number in range(1, total_lines + 1):
            line_content = self.textwidget.get(f"{line_number}.0", f"{line_number}.end")
            hash_position = line_content.find('#')
            if hash_position != -1:
                self.textwidget.delete(f"{line_number}.{hash_position}", f"{line_number}.end")




    def down_three_lines(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+3l"
        self.textwidget.mark_set(tk.INSERT, new_position)

        return "break"

    def back_four_chars(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "-5c"
        self.textwidget.mark_set(tk.INSERT, new_position)

        return "break"

    def ahead_four_chars(self, event=None):
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)

        return "break"

    def tag_alternating(self, event=None):
        for i in range(0, 27, 2):
            index = "1." + str(i)
            end = index + "+1c"
            self.textwidget.tag_add("odd", index, end)

        self.textwidget.tag_configure("odd", foreground="orange")

        return "break"

    def downlines(self):
        self.content = "self."
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+1l"
        self.textwidget.mark_set(tk.INSERT, new_position)

        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)
        self.textwidget.insert(new_position, self.content)

        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+1l"
        self.textwidget.mark_set(tk.INSERT, new_position)
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)
        self.textwidget.insert(END, self.content)
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+1l"
        self.textwidget.mark_set(tk.INSERT, new_position)
        current_cursor_index = str(self.textwidget.index(tk.INSERT))
        new_position = current_cursor_index + "+5c"
        self.textwidget.mark_set(tk.INSERT, new_position)
        self.textwidget.insert(new_position, self.content)

    def indent(self, textwidget):
        try:
            selected_text = self.textwidget.get("sel.first", "sel.last")
            if selected_text:
                # Add four spaces to the beginning of each line
                indented_text = "\n".join(
                    f"    {line}" for line in selected_text.split("\n")
                )
                self.textwidget.replace("sel.first", "sel.last", indented_text)
        except Exception as e:
            print(e)
    def dedent(self, textwidget):
        try:
            selected_text = self.textwidget.get("sel.first", "sel.last")
            if selected_text:
                # Remove four spaces from the beginning of each line if present
                dedented_text = "\n".join(
                    line[4:] if line.startswith("    ") else line
                    for line in selected_text.split("\n")
                )
                self.textwidget.replace("sel.first", "sel.last", dedented_text)
        except Exception as e:
            print(e)
            
    def insert_selfs(self, textwidget):
        try:
            self.textwidget = textwidget

            start_index = self.textwidget.index("sel.first")
            end_index = self.textwidget.index("sel.last")

            selected_text = self.textwidget.get(start_index, end_index)
            new_lines = [
                "self." + line.strip() if line.strip() else line
                for line in selected_text.split("\n")
            ]
            new_text = "\n".join(new_lines)

            self.textwidget.delete(start_index, end_index)
            self.textwidget.insert(start_index, new_text)

        except Exception as e:
            print(e)
    def insert_self_in_parentheses(self, textwidget):
        start_index = self.textwidget.index("sel.first")
        end_index = self.textwidget.index("sel.last")

        selected_text = self.textwidget.get(start_index, end_index)
        new_lines = []

        for line in selected_text.split("\n"):
            if line.strip():
                new_line = line.replace(
                    "():", "(self):")  # Replace () with (self)
            else:
                new_line = line
            new_lines.append(new_line)

        new_text = "\n".join(new_lines)
        self.textwidget.delete(start_index, end_index)
        self.textwidget.insert(start_index, new_text)

  
    def insert_at_cursor(self, textwidget):
        self.textwidget = textwidget
        word = self.insertentry.get()
        self.textwidget.insert(tk.INSERT, word)

    def pygameaspg(self):
        start_index = self.textwidget.index("sel.first")
        end_index = self.textwidget.index("sel.last")

        selected_text = self.textwidget.get(start_index, end_index)
        new_lines = []
        for line in lines:
            # Skip the original import statement if it exists
            if "import pygame" in line and not line.strip().startswith("#"):
                continue
            # Replace 'pygame' with 'pg' in the rest of the file
            line = line.replace("pygame", "pg")
            file.write(line)

    
   
    def read_file_and_remove_duplicates(self):
        filepath = askopenfilename(filetypes=[("Comma Separted Values", "*.csv"), ("All Files", "*.*"),])
        if not filepath:
            return 
       
        custom_string = ''
        
        
        with open(filepath, 'r') as file:
            lines = file.readlines()

        cleaned_lines = [line.strip() for line in lines if line.strip()]
        unique_lines = list(set(cleaned_lines))

        # Generating a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{custom_string}_{timestamp}.csv"

        # Create a list with formatted items
        formatted_items = [f"{custom_string}_{timestamp}_{item}" for item in unique_lines]

        with open(output_filename, 'w') as file:
            for item in formatted_items:
                file.write(f"{item}\n")
                
        print(formatted_items)
        return formatted_items

   
        fontbar = FontBar(self.parent,self.textwidget)

 
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
