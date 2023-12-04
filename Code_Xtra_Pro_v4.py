import tkinter as tk
from tkinter import ttk, INSERT,END,ANCHOR,font,Toplevel
from tkinter import Button, Frame, Entry, END, Canvas
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

from tkinter.font import Font, families
from string import punctuation
import subprocess
from collections import Counter
import re

import autopep8
from tkinter.scrolledtext import ScrolledText
import sys
import os
import runpy
from  auto8 import *
from txinfo import *
from fontbar import *
from compare import *
from unimake import *
from pyline import *
from py_dir_doc_helper import *

# What's new V2 - scrollbar for lb, sort button for lb,  resized textwidget and others

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.bar_frm = tk.Frame(self.parent, width=50, height=50)
        self.bar_frm.grid(row=0, column=0, sticky="ew")
        self.parent.columnconfigure(0, weight=1)  # This makes the column expandable
        
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=4, column=0)
        self.frm1 = ttk.Frame(self.notebook, width=50, height=40)
        self.notebook.add(self.frm1, text="View")
        self.txtfrm = tk.Frame(self.frm1, width=50, height=40)
        self.txtfrm.grid(row=0, column=2)
        self.tx = ScrolledText(self.txtfrm, bg="white", bd=12, height=35,width=60,)
        self.tx.grid(row=0, column=2,sticky="w")
        self.textwidget = self.tx
        self.fontbar = FontBar(self.bar_frm, self.textwidget)
      
        self.path = os.getcwd()
        self.lbfrm = tk.Frame(self.frm1, width=5, height=30)
        self.lbfrm.grid(row=0, column=1)
        self.lb = tk.Listbox(self.lbfrm, bg="cyan2", bd=12, width=35, height=35, exportselection=False, selectmode=tk.SINGLE,)
        self.lb.grid(row=0, column=0)
        self.lb.focus()
        self.binding()
        self.lb.configure(selectmode="")
        self.lb.bind("<Double-Button-1>", self.listing)
        self.lb.bind("<<ListboxSelect>>", self.showcontent)
        self.lb.bind("<Double-Button-2>", lambda event: self.run(self.lb))
        self.scrollbar = tk.Scrollbar(self.lbfrm, orient='vertical', command=self.lb.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # Set the Listbox's yscrollcommand to the Scrollbar's set
        self.lb.config(yscrollcommand=self.scrollbar.set)
        self.curtxt = None
        self.x = self.lb.curselection()
        self.fr_buttons = tk.Frame(self.frm1, relief=tk.RAISED)
        self.fr_buttons.grid(row=0,column=0,sticky="ns")
        self.btn_1 = tk.Button(self.fr_buttons, text="Change Dir", bd=3,command=self.newdirlist)
        self.btn_1.grid(row=1, column=0)
        self.btn_2 = tk.Button(self.fr_buttons,text="Refresh Dir List",bd=3,command=self.makedirlist)
        self.btn_2.grid(row=2, column=0)
        self.btn_3 = tk.Button(self.fr_buttons, text="Sort Filelist",bd=3, command=self.sort_lb)
        self.btn_3.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.btn_grab = tk.Button(self.fr_buttons, text="Send to Editor Tab",bd=6, command=self.ggtxt)
        self.btn_grab.grid(row=4, column=0)
        self.btn_grab2 = tk.Button(self.fr_buttons, text="Send to Text Tab", bd=6,command=self.ggtxt2)
        self.btn_grab2.grid(row=6,column=0)
        tk.Label(self.fr_buttons, text="Current Directory Path").grid(row=8, column=0)
        self.dirpath = tk.Entry(self.fr_buttons, bd=10, width=40)
        self.dirpath.grid(row=10,column=0)
        tk.Label(self.fr_buttons, text="To Insert Entry").grid(row=12, column=0)
        self.insertentry = tk.Entry(self.fr_buttons, bd=14)
        self.insertentry.grid(row=14, column=0)
        self.dirpath.insert(0, self.path)
        self.frm2 = ttk.Frame(self.notebook, width=60, height=50)
        self.notebook.add(self.frm2, text="Text")
        self.text1 = ScrolledText(self.frm2, height=30, width=70, bg="white", bd=10)
        self.text1.grid(row=4, column=1, sticky="nsew")
        self.text1.insert("1.0", "end-1c")
        self.frm3 = ttk.Frame(self.notebook, width=50, height=44)
        self.notebook.add(self.frm3, text="Editor")
        self.frm4 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm4, text="Compare Text")
        self.textcompare = TextFileComparator(self.frm4)
        self.textcompare.run()
        self.frm5 = ttk.Frame(self.notebook, width=50, height=600)
        self.notebook.add(self.frm5, text="Unicode_Generator")
        uni = UnicodeListGeneratorApp(self.frm5)
        self.frm6 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm6, text="Codefab")
        self.code = CodeEditorApp(self.frm6)
        self.frm7 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm7, text="Py Module Doc & Dir Helper")
        py_viewer = PyDDViewer(self.frm7)
        

        self.frm8 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm8, text="Run A Py PRG")
        self.txt = ScrolledText(self.frm8, height=30, width=40, bg="white", bd=10)
        self.txt.grid(row=2, column=2)
        self.runbtn = tk.Button(self.frm8, text="Select Python File Run", command=self.run_python_file)
        self.runbtn.grid(row=5, column=5)
        self.frm9 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm9, text="9")
        self.text2 = ScrolledText(self.frm3, height=40, width=60, bg="white", bd=10)
        self.text2.grid(row=5, column=1, sticky="nsew")
        self.text2.insert("1.0", "end-1c")
##        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.frm10 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm10, text="PEP8")
        self.autopep8 = AutoPEP8Formatter(self.frm10)
        self.info1 = TextWidget_Info(self.frm1, self.tx)
        self.info2 = TextWidget_Info(self.frm2, self.text1)
        self.info3 = TextWidget_Info(self.frm3, self.text2)
        self.textwidgets = [self.tx, self.text1, self.text2]
        self.fontbar = FontBar(self.bar_frm,self.textwidget)
        self.menubar = tk.Menu(self.parent, tearoff=False)
        
        self.file_menu = tk.Menu(self.menubar)
        self.edit_menu = tk.Menu(self.menubar)
        self.view_menu = tk.Menu(self.menubar)
        self.cursor_menu = tk.Menu(self.menubar)
        self.format_menu = tk.Menu(self.menubar)
        self.tool_menu = tk.Menu(self.menubar)

        self.listing()
        
        self.text = self.textwidget.get("1.0", "end-1c")
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
        self.file_menu.add_command(label="-----", underline=1, command=self.quit)
        self.file_menu.add_command(label="-------", underline=1, command=self.quit)
        self.file_menu.add_command(label="Exit", underline=1, command=self.exit_application)
###################
        self.add_cascade(label="Edit", menu=self.edit_menu)
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
            command=lambda: self.find(),
        )
        self.edit_menu.add_command(
            label="Replace",
            accelerator="Ctrl+R",
            compound="left",
            underline=0,
            command=lambda: self.replace(),
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
        command=lambda : self.insert_self_in_parentheses(self.textwidget),
        )
        self.format_menu.add_command(
        label="Auto PEP Format",
        compound="left",
        underline=0,
        command=self.format_file,
        )
        self.format_menu.add_command(
        label="-----",
        compound="left",
        underline=0,
        command=None
        )
        self.format_menu.add_command(
        label=" pygameaspg",
        compound="left",
        underline=0,
        command=self.pygameaspg
        )
       
        self.format_menu.add_command(
        label="Remove Comments",
        compound="left",
        underline=0,
        command=self.remove_comments,
        )
        self.format_menu.add_command(
        label="Insert a Prefix",
        compound="left",
        underline=0,
        command=lambda: self.insert_prefix(self.textwidget),
        )
        self.format_menu.add_command(
        label="Insert at Cursor",
        compound="left",
        underline=0,
        command= lambda: self.insert_at_cursor(self.textwidget),
        )
        self.format_menu.add_command(
        label="-Insert Suffix",
        compound="left",
        underline=0,
        command=lambda: self.insert_suffix(self.textwidget),
        )

        self.binding()
        self.makedirlist()
        self.update_info()
##############################################################################
####################### METHODS ##############################################

    def remove_comments(self, file_path):
          self.open_file()
          with open(file_path, 'r') as file:
              lines = file.readlines()
              new_lines = []
              for line in lines:
                  if '#' in line and not (line.strip().startswith("'") or line.strip().startswith('"')):
                      new_line = line.split('#')[0]
                      new_lines.append(new_line.rstrip() + '\n')
                  else:
                      new_lines.append(line)
          self.save_file()
          with open(file_path, 'w') as file:
              file.writelines(new_lines)

    def makedirlist(self):
        self.path = os.getcwd()
        self.dirpath.delete(0, tk.END)
        self.dirpath.insert(tk.END, self.path)

    def newdirlist(self):
        self.path = askdirectory()
        if self.path:  # Check if a directory was selected
            os.chdir(self.path)
            self.listing()

    def listing(self, event=None):
        self.flist = os.listdir(self.path)
        self.lb.delete(0, tk.END)  # Clear ListBox
        for item in self.flist:
            if item.endswith((".py", ".txt")):
                
                self.lb.insert(tk.END, item)
        
        self.dirpath.delete(0, tk.END)
        self.dirpath.insert(0, self.path)
        self.lb.bind("<<ListboxSelect>>", self.showcontent)

    def showcontent(self, event=None):
        selected_index = self.lb.curselection()
        if selected_index:
            file_path = os.path.join(self.path, self.lb.get(selected_index[0]))
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as file_content:
                        content = file_content.read()
                        self.textwidget.delete("1.0", tk.END)
                        self.textwidget.insert(tk.END, content)
                except Exception as e:
                # Handle exceptions, maybe show a message to the user
                    print(f"Error opening file: {e}")
            else:
            # Handle the case where the file does not exist
                print("Selected file does not exist.")



    
    def update_info(self):
       
        self.info1.update_info()
        self.info2.update_info()
        self.info3.update_info()
                

    

    def ggtxt(self):
        #send to to another textwidget
      
        gettxt = self.tx.get("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.text2.insert(tk.END, gettxt)

    
    def ggtxt2(self):
        #send to to another textwidget
      
        gettxt = self.tx.get("1.0", tk.END)
        self.text1.delete("1.0", tk.END)
        self.text1.insert(tk.END, gettxt)

    def run_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.txt.delete(1.0, tk.END) 
        try:
            # Attempt to run the script
            runpy.run_path(file_path)
        except Exception as e:
            # If an error occurs, display it in the text widget
            self.txt.insert(tk.END, f"An error occurred: {e}\n")

                       
           
    def on_tab_changed(self, event=None):
        # Get the currently selected tab index
        selected_index = self.notebook.index(self.notebook.select())
        
        # Assign the corresponding text widget to self.textwidget
        if selected_index == 0:  # Assuming this index corresponds to self.frm1
            self.textwidget = self.tx
            
        elif selected_index == 1:  # Assuming this index corresponds to self.frm2
            self.textwidget = self.text1
            FontBar(self.bar_frm, self.textwidget)
        elif selected_index == 2:  # Assuming this index corresponds to self.frm3
            self.textwidget = self.text2
            FontBar(self.bar_frm, self.textwidget)
        elif selected_index == 5:  # Assuming this index corresponds to self.frm6
            self.textwidget = self.code.textwidget
            FontBar(self.bar_frm, self.textwidget)
        elif selected_index == 7:
            self.textwidget = self.txt
            FontBar(self.bar_frm, self.textwidget)
        else:
            self.textwidget = None  # or any default widget
    def can_respond(self, widget):
        # Check if the widget is enabled
        if str(widget['state']) == 'disabled':
            return False

        # Check if the widget is visible
        if not widget.winfo_ismapped():
            return False

        # Check for specific content conditions
        content = widget.get("1.0", "end-1c")
        if some_specific_condition(content):  # Replace with your condition
            return False

        # Check if the widget has focus
        if widget is not self.focus_get():
            return False

        return True


    def sort_lb(self):
        # Retrieve and sort the lb items
        items = list(self.lb.get(0, tk.END))
        items.sort()

        # Update the lb with sorted items
        self.lb.delete(0, tk.END)  # Clear current items
        for item in items:
            self.lb.insert(tk.END, item)




    def cursor_to_top(self):
        self.textwidget.mark_set("insert", "1.0")
        self.textwidget.see("insert")
    def cursor_to_bottom(self):
        self.textwidget.mark_set("insert", "end-1c")
        self.textwidget.see("insert")

    def cleartags(self):
        self.textwidget.tag_config("found", foreground="black", background="white")
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
        filepath = asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"),("Text Files", "*.txt"), ("All Files", "*.*")],
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
            self.textwidget.insert(tk.END, text)
            return filepath2

    def find(self):
        top = Toplevel()
        label1 = tk.Label(top, text="Find").grid(row=1, column=1)
        entry1 = tk.Entry(top, width=15, bd=12, bg="cornsilk")
        entry1.grid(row=2, column=1)

        def finder():
            # remove tag 'found' from index 1 to END
            self.textwidget.tag_remove("found", "1.0", END)
            entry = entry1.get()

            if entry1:
                idx = "1.0"
                while 1:
                    # searches for desired string from index 1
                    idx = self.textwidget.search(entry, idx, nocase=1, stopindex=END)

                    if not idx:
                        break

                    # last index sum of current index and
                    # length of text
                    lastidx = "% s+% dc" % (idx, len(entry))

                    # overwrite 'Found' at idx
                    self.textwidget.tag_add("found", idx, lastidx)
                    idx = lastidx

                # mark located string as red

                self.textwidget.tag_config(
                    "found", background="purple", foreground="yellow"
                )

        self.find_btn = tk.Button(top, text="Find", bd=8, command=finder)
        self.find_btn.grid(row=8, column=1)
        entry1.focus_set()

    def replace(self):
        top = Toplevel()
        label1 = tk.Label(top, text="Find").grid(row=1, column=1)
        entry1 = tk.Entry(top, width=15, bd=12, bg="cornsilk")
        entry1.grid(row=2, column=1)
        label2 = tk.Label(top, text="Replace With ").grid(row=3, column=1)
        entry2 = tk.Entry(top, width=15, bd=12, bg="seashell")
        entry2.grid(row=5, column=1)

        def replacer():
            # remove tag 'found' from index 1 to END
            self.textwidget.tag_remove("found", "1.0", END)

            # returns to widget currently in focus
            self.fin = entry1.get()
            self.repl = entry2.get()

            if self.fin and self.repl:
                idx = "1.0"
                while 1:
                    # searches for desired string from index 1
                    idx = self.textwidget.search(self.fin, idx, nocase=1, stopindex=END)
                    print(idx)
                    if not idx:
                        break

                    # last index sum of current index and
                    # length of text
                    lastidx = "% s+% dc" % (idx, len(self.fin))

                    self.textwidget.delete(idx, lastidx)
                    self.textwidget.insert(idx, self.repl)

                    lastidx = "% s+% dc" % (idx, len(self.repl))

                    # overwrite 'Found' at idx
                    self.textwidget.tag_add("found", idx, lastidx)
                    idx = lastidx

            
            self.textwidget.tag_config("found", foreground="green", background="yellow")

        self.replace_btn = tk.Button(top, text="Find & Replace", bd=8, command=replacer)
        self.replace_btn.grid(row=8, column=1)
        entry1.focus_set()

   

    def toggle_highlight(self, event=None):
        val = hltln.get()

        undo_highlight() if not val else highlight_line()

    def undo_highlight(self):
        self.self.textwidget.tag_remove("active_line", "1.0", tk.END)

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
        selected_text = textwidget.get("sel.first", "sel.last")
        if selected_text:
            # Add four spaces to the beginning of each line
            indented_text = "\n".join(
                f"    {line}" for line in selected_text.split("\n")
            )
            textwidget.replace("sel.first", "sel.last", indented_text)

    def dedent(self,textwidget):
        selected_text = textwidget.get("sel.first", "sel.last")
        if selected_text:
            # Remove four spaces from the beginning of each line if present
            dedented_text = "\n".join(
                line[4:] if line.startswith("    ") else line
                for line in selected_text.split("\n")
            )
            textwidget.replace("sel.first", "sel.last", dedented_text)

    

  
    def insert_selfs(self, textwidget):
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

    def insert_self_in_parentheses(self, textwidget):
        start_index = textwidget.index("sel.first")
        end_index = textwidget.index("sel.last")

        selected_text = textwidget.get(start_index, end_index)
        new_lines = []

        for line in selected_text.split("\n"):
            if line.strip():
                new_line = line.replace("()", "(self)")  # Replace () with (self)
            else:
                new_line = line
            new_lines.append(new_line)

        new_text = "\n".join(new_lines)
        textwidget.delete(start_index, end_index)
        textwidget.insert(start_index, new_text)
     

    def insert_prefix(self, textwidget):
         
        self.textwidget = textwidget
        prefix = self.insertentry.get()
        start_index = self.textwidget.index("sel.first")
        end_index = self.textwidget.index("sel.last")

        selected_text = self.textwidget.get(start_isuffixndex, end_index)
        new_lines = [
            prefix + line.strip() if line.strip() else line
            for line in selected_text.split("\n")
        ]
        new_text = "\n".join(new_lines)

        self.textwidget.delete(start_index, end_index)
        self.textwidget.insert(start_index, new_text)

    def insert_suffix(self, textwidget):
        self.textwidget = textwidget
        suffix = self.insertentry.get()
        start_index = self.textwidget.index("sel.first")
        end_index = self.textwidget.index("sel.last")
        selected_text = self.textwidget.get(start_index, end_index)
        new_lines = [
            line.strip() + suffix if line.strip() else line
            for line in selected_text.split("\n")
        ]
        new_text = "\n".join(new_lines)
        self.textwidget.delete(start_index, end_index)
        self.textwidget.insert(start_index, new_text)

    def insert_at_cursor(self, textwidget):
        self.textwidget = textwidget
        word = self.insertentry.get()
        self.textwidget.insert(tk.INSERT, word)

    def binding(self):
        self.lb.bind("<Double-Button-1>", self.listing)
        self.lb.bind("<<ListboxSelect>>", self.showcontent)
        self.lb.bind("<<ListboxSelect>>", lambda event: self.listing(event))
       

        self.textwidget.bind("<Control-h>", self.highlight_line)
        self.textwidget.bind("<Control-w>", self.highlight_word)
        self.textwidget.bind("<Control-d>", self.down_three_lines)
        self.textwidget.bind("<Control-b>", self.back_four_chars)
        self.textwidget.bind("<Control-t>", self.tag_alternating)

    def pygameaspg(self):
        start_index = textwidget.index("sel.first")
        end_index = textwidget.index("sel.last")

        selected_text = textwidget.get(start_index, end_index)
        new_lines = []
        for line in lines:
            # Skip the original import statement if it exists
            if "import pygame" in line and not line.strip().startswith("#"):
                continue
            # Replace 'pygame' with 'pg' in the rest of the file
            line = line.replace("pygame", "pg")
            file.write(line)




class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
