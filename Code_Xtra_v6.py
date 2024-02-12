import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, INSERT, END, ANCHOR, font, Toplevel
from tkinter import Button, Frame, Entry, END, Canvas, Scrollbar
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from datetime import datetime
from tkinter.font import Font, families
from string import punctuation
import subprocess
from collections import Counter
import re
import pylint
import autopep8
import sys
import os
import runpy
import re
####User Modules#####
from auto8 import *
from txinfo import *
from compare import *
from unimake import *
from pyline import *
from py_dir_doc_helper import *
from filefnr import *
from newadd import *
from remove_stuff import *
# What's new V2 - scroltreeviewar for treeview, sort button for treeview,  resized textwidget and others
# added multi-file find and replace app
#camel case to snake case and remove line is word exist

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.bar_frm = tk.Frame(self.parent)
        self.bar_frm.grid(row=0, column=0, sticky="ew")
        self.parent.columnconfigure(0, weight=1)
    

        # Notebook setup
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.parent.rowconfigure(1, weight=1)

        self.frm1 = ttk.Frame(self.notebook)
        self.notebook.add(self.frm1, text="View")

        # Frames inside frm1 for different sections
        self.txtfrm = tk.Frame(self.frm1)
        self.txtfrm.grid(row=0, column=2, sticky="nsew")
        self.frm1.columnconfigure(2, weight=3)

        self.tx = ScrolledText(self.txtfrm, bg="white", bd=12)
        self.tx.grid(row=0, column=1, sticky="nsew")
        self.txtfrm.rowconfigure(0, weight=1)
        self.textwidget = self.tx

        self.path = os.getcwd()
        self.tree_frame = tk.Frame(self.frm1)
        self.tree_frame.grid(row=0, column=1, sticky="nsew")

        # Update columns to include file size and date added
        self.columns = ("filename", "size", "modified")
        self.treeview = ttk.Treeview(
            self.tree_frame,
            columns=self.columns,
            show="headings")
        self.treeview.grid(row=0, column=1, sticky="nsew")
        self.frm1.columnconfigure(1, weight=1)

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
        self.fr_buttons = tk.Frame(self.frm1)
        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.frm1.columnconfigure(0, weight=1)
        # Auto-indent toggle checkbox
##        self.auto_indent_var = tk.BooleanVar(value=True)  # Auto-indent is enabled by default
##        self.auto_indent_checkbox = tk.Checkbutton(self.fr_buttons, text="Enable Auto-Indent", var=self.auto_indent_var, command=self.toggle_auto_indent)
##        self.auto_indent_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.btn_1 = tk.Button(
            self.fr_buttons,
            text="Change Dir",
            bd=3,
            command=self.newdirlist)
        self.btn_1.grid(row=2, column=0)
        
        self.btn_grab = tk.Button(
            self.fr_buttons,
            text="Send to Editor Tab",
            bd=6,
            command=self.ggtxt)
        self.btn_grab.grid(row=4, column=0)
        self.btn_grab2 = tk.Button(
            self.fr_buttons,
            text="Send to Text Tab",
            bd=6,
            command=self.ggtxt2)
        self.btn_grab2.grid(row=5, column=0)
        
        self.frm2 = ttk.Frame(self.notebook, width=60, height=50)
        self.notebook.add(self.frm2, text="Text")
        self.text1 = ScrolledText(
            self.frm2,
            height=30,
            width=120,
            bg="white",
            bd=10)
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
        
        self.txt = ScrolledText(
            self.frm8,
            height=30,
            width=40,
            bg="white",
            bd=10)
        self.txt.grid(row=2, column=2)
        self.runbtn = tk.Button(
            self.frm8,
            text="Select Python File Run",
            command=self.run_python_file)
        self.runbtn.grid(row=5, column=5)
        self.frm9 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm9, text="PYlint")
        self.text2 = ScrolledText(
            self.frm3,
            height=40,
            width=120,
            bg="white",
            bd=10)
        self.text2.grid(row=5, column=1, sticky="nsew")
        self.text2.insert("1.0", "end-1c")

        
        self.frm10 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm10, text="PEP8")
        self.autopep8 = AutoPEP8Formatter(self.frm10)
        self.frm11 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm11, text="MultiFile Find&Replace")
        self.filefindreplace = FindReplaceApp(self.frm11)
        self.info1 = TextWidget_Info(self.frm1, self.tx)
        self.info2 = TextWidget_Info(self.frm2, self.text1)
        self.info3 = TextWidget_Info(self.frm3, self.text2)
        self.textwidgets = [self.tx, self.text1, self.text2]
        self.frm12 = ttk.Frame(self.notebook, width=50, height=60)
        self.notebook.add(self.frm12, text="Rmv_Line #")
        self.remove_line_numbers = remove_add(self.frm12)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.menubar = tk.Menu(self.parent, tearoff=False)
        self.binding()
        self.file_menu = tk.Menu(self.menubar)
        self.edit_menu = tk.Menu(self.menubar)
        self.view_menu = tk.Menu(self.menubar)
        self.cursor_menu = tk.Menu(self.menubar)
        self.format_menu = tk.Menu(self.menubar)
      
        self.text3 = ScrolledText(
            self.frm9,
            height=40,
            width=100,
            bg="white",
            bd=10)
        self.text3.grid(row=5, column=1, sticky="nsew")
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
            command=lambda: self.insert_self_in_parentheses(self.textwidget),
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
            label="Insert a Prefix",
            compound="left",
            underline=0,
            command=lambda: self.insert_prefix(self.textwidget),
        )
        self.format_menu.add_command(
            label="Insert at Cursor",
            compound="left",
            underline=0,
            command=lambda: self.insert_at_cursor(self.textwidget),
        )
        self.format_menu.add_command(
            label="-Insert Suffix",
            compound="left",
            underline=0,
            command=lambda: self.insert_suffix(self.textwidget))

        self.format_menu.add_command(
            label="CamelCase to snake_case",
            compound="left",
            underline=0,
            command=self.convert_to_snake_case
        )
        self.format_menu.add_command(
            label="Remove Line Containing",
            compound="left",
            underline=0,
            command=self.remove_lines_containing
        )

        self.format_menu.add_command(
            label="Pylint a script",
            compound="left",
            underline=0,
            command=self.run_pylint,
        )

        
        self.binding()
        self.makedirlist()
        self.update_info()
    ##############################################################################
####################### METHODS ##############################################
    def on_dir_selected(self, event=None):
        selection = self.pm.lbpath.curselection()
        if selection:
            index = selection[0]
            dir_path = self.pm.lbpath.get(index)
            # Update the file browser view to reflect the selected directory
            # This is a placeholder - you'll need to implement the actual update logic
            print(f"Directory selected: {dir_path}")
            self.get_selected_path()
           # Example: update_directory_view(dir_path)

           # Example function to add current directory to pm.lbpath 
    def add_current_dir_to_listbox(self):
        current_dir = os.getcwd()  # Get the current working directory
        self.pm.lbpath.insert(tk.END, current_dir)  # Add to the listbox
        # Optionally, save the list to a file or database for persistence
    
        # Binding the listbox click event
        self.pm.lbpath.bind('<Double-1>', self.on_dir_selected)

        # Assuming you have a button or method to call `add_current_dir_to_listbox`
       
    def toggle_auto_indent(self):
        # Change settings or update UI based on the auto-indent feature's state
        if self.auto_indent_var.get():
            # Auto-indent is enabled
            self.textwidget.config(bg="alice blue")  # Set background
            print("Auto-indent enabled")  # Or update a status label in the UI
        else:
            # Auto-indent is disabled
            self.textwidget.config(bg="white")  # Set background to a ate disabled state
            print("Auto-indent disabled")
    def auto_indent(self, event):
        if self.auto_indent_var.get():  # Check if auto-indent is enabled
            line = self.textwidget.get("insert linestart", "insert lineend")
            if line.strip().endswith(":"):
                self.textwidget.insert("insert", "\n" + " " * 4)
                return "break"  # Prevents the default newline behavior

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

      
    def getfile(self):
        filename = askopenfilename(
            filetypes=[
                ("Python Scripts", "*.py"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ]
        )
        if not filename:
            return
        else:
            result = subprocess.run(
                ["pylint", filename], capture_output=True, text=True)
            print(result.stdout)
            self.text3.insert(tk.END, result)
        if result.stderr:
            print("Error:", result.stderr)

    def makedirlist(self):
        self.path = os.getcwd()
        self.listing()

    def newdirlist(self):
        self.path = askdirectory()
        if self.path:  # Check if a directory was selected
            os.chdir(self.path)
         
            self.listing()

    def listing(self, event=None):
        self.flist = os.listdir(self.path)
        self.treeview.delete(*self.treeview.get_children()
                             )  # Clear the Treeview
        for item in self.flist:
            if item.endswith((".py", ".txt")):
                file_size = os.path.getsize(item)  # Example for file size
                modified_timestamp = os.path.getmtime(item)
                modified_date = datetime.fromtimestamp(modified_timestamp).strftime(
                    '%Y-%m-%d %H:%M:%S')  # Formatted date

                # Inserting into the Treeview
                self.treeview.insert(
                    '', 'end', values=(
                        item, file_size, modified_date))

     

    def showcontent(self, event=None):
        selected_item = self.treeview.selection()
        if selected_item:
            file_name = self.treeview.item(selected_item[0])['values'][0]
            file_path = os.path.join(self.path, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as file_content:
                        content = file_content.read()
                        self.textwidget.delete("1.0", tk.END)
                        self.textwidget.insert(tk.END, content)
                except Exception as e:
                    print(f"Error opening file: {e}")
            else:
                print("Selected file does not exist.")

    def update_info(self):

        self.info1.update_info()
        self.info2.update_info()
        self.info3.update_info()

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
        # send to to another textwidget

        gettxt = self.tx.get("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.text2.insert(tk.END, gettxt)

    def ggtxt2(self):
        # send to to another textwidget

        gettxt = self.tx.get("1.0", tk.END)
        self.text1.delete("1.0", tk.END)
        self.text1.insert(tk.END, gettxt)

    def run_python_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py")])
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
        
        # Initialize textwidget as None
        self.textwidget = None

        # Assign the corresponding text widget to self.textwidget based on the selected tab
        if selected_index == 0:
            self.textwidget = self.tx
        elif selected_index == 1:
            self.textwidget = self.text1
        elif selected_index == 2:
            self.textwidget = self.text2
        elif selected_index == 5:
            self.textwidget = self.code.textwidget
        elif selected_index == 7:
            self.textwidget = self.txt

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
                while True:
                    # searches for desired string from index 1
                    idx = self.textwidget.search(
                        entry, idx, nocase=1, stopindex=END)

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
                while True:
                    # searches for desired string from index 1
                    idx = self.textwidget.search(
                        self.fin, idx, nocase=1, stopindex=END)
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

            self.textwidget.tag_config(
                "found", foreground="green", background="yellow")

        self.replace_btn = tk.Button(
            top, text="Find & Replace", bd=8, command=replacer)
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

            formatted_code = autopep8.fix_code(
                original_code, options={'aggressive': 1})

            if original:
                base, ext = os.path.splitext(file_path)
                new_file_path = f"{base}_formatted{ext}"
                with open(new_file_path, 'w') as file:
                    file.write(formatted_code)
                self.output(
                    f"Formatted and saved as new file: {os.path.basename(new_file_path)}")
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
    def convert_to_snake_case(self):
        text = self.textwidget.get("1.0", tk.END)
        # Regular expression to identify camelCase words
        snake_case_text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
        self.textwidget.delete("1.0", tk.END)  # Clear the text widget
        self.textwidget.insert("1.0", snake_case_text)  # Insert the modified text


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

    def dedent(self, textwidget):
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
                new_line = line.replace(
                    "():", "(self):")  # Replace () with (self)
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
        self.treeview.bind("<<TreeviewSelect>>", self.showcontent)
        self.treeview.bind("<Double-Button-1>", self.on_double_click)

      
  
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

    def run_pylint(self):
        filename = askopenfilename(filetypes=[("Python Scripts", "*.py"),
                                              ("Text Files", "*.txt"),
                                              ("All Files", "*.*"),
                                              ]
                                   )
        if not filename:
            return
        result = subprocess.run(['pylint', filename],
                                capture_output=True, text=True)
        print(run_pylint('my_script.py'))
        return result.stdout


 
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
