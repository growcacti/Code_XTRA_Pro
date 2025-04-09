import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, font, Toplevel, font, Scrollbar
from tkinter.scrolledtext import ScrolledText
from tkinter.colorchooser import askcolor
import re
import time
import sys
import json
import subprocess
import runpy
import pyperclip
from datetime import datetime
from pylint.lint import Run
from io import StringIO
import autopep8, black, pylint
import random
import logging

#Menu edit and formatter mostly fixed
#tk widget edits
#should be most up to date version
#lines word count restored



class MultiTabTextEditor:
    def __init__(self, root):
        self.root = root
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.tabs = []  # List to keep track of tabs
        self.path = os.getcwd()
        self.file_name = None
        self.program_name = "PyCode Tabbed Editor"
        self.history_file = "file_history.json"
        self.file_history = self.load_file_history()
        self.current_font_family = tk.StringVar(value="")
        self.current_font_size = tk.StringVar(value="9")
        self.history_file = "file_history.json"
        self.file_history = self.load_file_history()
        self.style = ttk.Style()
        self.style.configure("TNotebook", background="skyblue", borderwidth=8)
        self.style.theme_create("hewitt", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1]},
                "map": {"background": [("selected", "medium spring green")]}
            }
        })
        self.style.theme_use("hewitt")
      
        # Configure row and column weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.add_tab()  
        # Menu bar
        self.menubar = tk.Menu(self.root,background ="SkyBlue2")
        self.root.config(menu=self.menubar)
        root.option_add("*Menu.font", "Verdana 8 bold")
        # File menu
        self.file_menu = tk.Menu(self.menubar, background="CadetBlue2",tearoff=0)
        self.file_menu.add_command(label="New Tab", command=self.add_tab)
        self.file_menu.add_command(label="Close Tab", command=self.remove_current_tab)
        self.file_menu.add_command(label="Open File", command=self.openfile)
        self.file_menu.add_command(label="Save File", command=self.savefile)
        self.file_menu.add_command(label="Save File As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.file_menu.add_separator()
        self.recent_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Recently Loaded", menu=self.recent_menu)
        self.file_menu.add_command(label="Readlines", command=self.readlines)
        self.file_menu.add_command(
            label="Save Version", command=self.save_incremented_version
        )
        self.file_menu.add_command(
            label="Run File", accelerator="F5", command=self.run_file
        )
        self.file_menu.add_command(
            label="Run File", accelerator="F10", command=self.run_py_file
        )
        self.file_menu.add_command(
            label="Exit", accelerator="Alt+F4", command=self.quit
        )
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menubar,background="PaleGreen3", tearoff=0)
        self.edit_menu.add_separator()  # Group separator
        
        self.edit_menu.add_command(
            label="Move to Next Tab", command=self.move_to_next_tab
        )
        self.edit_menu.add_command(
            label="Move to Previous Tab", command=self.move_to_previous_tab
        )
        self.edit_menu.add_command(
            label="Copy to Next Tab", command=self.copy_to_next_tab
        )
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+x", command=self.cut)
        self.edit_menu.add_command(
            label="Copy", accelerator="Ctrl+c", command=self.copy
        )
        self.edit_menu.add_separator()  # Group separator
        self.edit_menu.add_command(
            label="Paste", accelerator="Ctrl+v", command=self.paste
        )
        self.edit_menu.add_command(
            label="Select All", accelerator="Ctrl+a", command=self.select_all
        )
        self.edit_menu.add_command(
            label="Clipboard Clear", accelerator="Ctrl+2", command=self.clear_clipboard
        )
        self.edit_menu.add_command(
            label="Undo", accelerator="Ctrl+z", command=self.undo
        )
        self.edit_menu.add_command(
            label="Redo", accelerator="Ctrl+y", command=self.redo
        )
        self.edit_menu.add_command(
            label="Find Replace", accelerator="Ctrl+f", command=self.find_replace
        )
        self.edit_menu.add_command(
            label="Highlight Section", command=self.highlight_section
        )
        self.edit_menu.add_command(label="Highlight Line", command=self.highlight_line)
        self.edit_menu.add_command(label="Undo Highlight", command=self.undo_highlight)
        self.edit_menu.add_command(
            label="Indent",
            accelerator="Ctrl+]",
            command=lambda: self.indent(self.textwidget),
        )
        self.edit_menu.add_command(
            label="Dedent",
            accelerator="Ctrl+[",
            command=lambda: self.dedent(self.textwidget),
        )
        self.edit_menu.add_command(
            label="Comment Out", accelerator="Ctrl+/", command=self.comment_out_selected
        )
        self.edit_menu.add_command(
            label="Remove Stand Alone Comments", command=self.remove_standalone_comments
        )
        self.edit_menu.add_command(
            label="Remove Comments", command=self.remove_comments
        )
        self.edit_menu.add_command(
            label="Remove_Text_Between_Quotes", command=self.remove_text_between_quotes
        )
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        # View menu
        self.view_menu = tk.Menu(self.menubar, background="plum3", tearoff=0)
        self.showln = tk.IntVar()
        self.showln.set(1)
        self.syn = tk.IntVar()
        self.syn.set(1)
        self.hltln = tk.IntVar()

        self.view_menu.add_checkbutton(
            label="Highlight Current Line",
            variable=self.hltln,
            command=self.toggle_highlight,
        )
        self.view_menu.add_checkbutton(
            label="Snytax Highlighting",
            variable=self.syn,
            command=self.highlight_active_tab,
        )
        self.view_menu.add_command(
            label="Search & Highlight", command=self.search_output
        )
        self.view_menu.add_command(label="Background Color", command=self.change_bg)
        self.view_menu.add_command(label="Foreground Color", command=self.change_fg)
        self.view_menu.add_command(label="Cursor Update", command=self.update_info)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        # Format menu
        self.format_menu = tk.Menu(self.menubar, background="dark salmon",tearoff=0)
        self.format_menu.add_command(label="Bold", command=lambda: self.toggle_bold())
        self.format_menu.add_command(
            label="Italic", command=lambda: self.toggle_italic()
        )
        self.format_menu.add_command(
            label="Underline", command=lambda: self.toggle_underline()
        )
        self.format_menu.add_command(
            label="Highlight", command=lambda: self.toggle_highlight()
        )
        self.format_menu.add_command(label="Choose Font", command=self.choose_font)
        self.format_menu.add_command(
            label="Justify Left", command=lambda: self.align_left(self.textwidget)
        )
        self.format_menu.add_command(
            label="Justify Center", command=lambda: self.align_center(self.textwidget)
        )
        self.format_menu.add_command(
            label="Justify Right", command=lambda: self.align_right(self.textwidget)
        )


        self.format_menu.add_command(label="Format & Lint Code", command=lambda:self.open_formatter_tab(self.textwidget))



        self.menubar.add_cascade(label="Format", menu=self.format_menu)
        # Custom menu
        self.custom_menu = tk.Menu(self.menubar,background="aquamarine", tearoff=0)
        self.custom_menu.add_command(
            label="Insert selfs on selected make oop ",
            command=lambda: self.insert_selfs(self.textwidget),
        )
        self.custom_menu.add_command(
            label="Functions to Method on selection",
            command=lambda: self.in_parentheses(self.textwidget),
        )
        self.custom_menu.add_command(
            label="Functions to Method All",
            command=lambda: self.in_entire_text(self.textwidget),
        )
        self.custom_menu.add_command(
            label="imsert word at cursor",
            command=lambda: self.at_cursor(self.textwidget),
        )
        self.custom_menu.add_command(
            label="Move Imports to Top", command=self.move_imports_to_top
        )
        self.custom_menu.add_command(
            label="Remove Text Between Single Quotes",
            command=lambda: self.remove_text_between_quotes("single"),
        )
        self.custom_menu.add_command(
            label="Remove Text Between Double Quotes",
            command=lambda: self.remove_text_between_quotes("double"),
        )
        self.custom_menu.add_command(
            label="Remove Text Between Triple Quotes",
            command=lambda: self.remove_text_between_quotes("triple"),
        )
        self.custom_menu.add_command(
            label="Remove Text Between All Quotes",
            command=lambda: self.remove_text_between_quotes("all"),
        )
        self.custom_menu.add_command(
            label="Color Buttons Selection", command=lambda: self.show_color_selector()
        )
        self.custom_menu.add_command(
            label="Quik Reader", command=lambda: self.filelist(self.path)
        )
        self.menubar.add_cascade(label="Custom", menu=self.custom_menu)

        # About menu
        self.about_menu = tk.Menu(self.menubar, background="DarkOrchid1",tearoff=0)
        self.about_menu.add_command(label="About", command=self.about)
        self.about_menu.add_command(label="Help", command=self.help)
        self.menubar.add_cascade(label="About", menu=self.about_menu)

        self.update_recent_menu()
        self.root.config(menu=self.menubar)

    def bind_shortcuts(self):
        self.textwidget.bind("<Control-y>", self.redo)
        self.textwidget.bind("<Control-Y>", self.redo)
        self.textwidget.bind("<Control-A>", self.select_all)
        self.textwidget.bind("<Control-a>", self.select_all)
        self.textwidget.bind("<Control-f>", self.find_replace)
        self.textwidget.bind("<Control-F>", self.find_replace)
        self.textwidget.bind("<Control-o>", self.openfile)
        self.textwidget.bind("<Control-O>", self.openfile)
        self.textwidget.bind("<Control-s>", self.savefile)
        self.textwidget.bind("<Control-S>", self.savefile)
        self.textwidget.bind("<Shift-Control-S>", self.save_file_as)
        self.textwidget.bind("<Shift-Control-s>", self.save_file_as)
        self.textwidget.bind("<Control-n>", self.newfile)
        self.textwidget.bind("<Control-N>", self.newfile)
        self.textwidget.bind("<KeyPress-F1>", self.help)
        self.textwidget.bind("<Any-KeyPress>", self.on_content_changed)
        self.textwidget.bind("<KeyRelease>", self.update_info)
        self.textwidget.bind("<ButtonRelease>", self.update_info)
        self.textwidget.bind(
            "<Control-slash>", lambda event: self.comment_out_selected()
        )
        self.textwidget.bind("<Control-bracketright>", self.indent)
        self.textwidget.bind("<Control-bracketleft>", self.dedent)

    def quit(self):
        if self.root.winfo_exists():  # Check if the window still exists
            try:
                if messagebox.askokcancel("Quit?", "Exit Program"):
                    self.root.quit()
                    self.root.destroy()
            except Exception as e:
                print(f"Error during quit: {e}")


    def add_tab(self):
        tab = ttk.Frame(self.notebook)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        self.textwidget = ScrolledText(tab, bd=12,bg="light cyan", wrap="word", font=("Consolas", 12))
        self.textwidget.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.info_label = tk.Label(tab, text="Lines: 0  \n | Words: 0   \n| Characters: 0 \n| Cursor Position: Line 1   , Column 0       ")
        self.info_label.grid(row=40, column=0)
        self.textwidget.bind("<KeyRelease>", self.update_info)
        self.textwidget.bind("<ButtonRelease-1>", self.update_info)
        self.textwidget.bind("<<Modified>>", self.on_text_modified)
        self.textwidget.bind("<ButtonRelease-2>", self.update_info)
   

        # Add SyntaxHighlite to this textwidget
        SyntaxHighlite(self.textwidget)

        self.notebook.add(tab, text=f"Tab {len(self.tabs) + 1}")
        self.tabs.append(self.textwidget)
        self.notebook.select(len(self.tabs) - 1)
        self.style.configure("TNotebook.Tab", background="yellow green")

    def remove_current_tab(self):
        """Remove the currently selected tab."""
        if len(self.tabs) > 1:  # Ensure at least one tab remains
            current_tab_index = self.notebook.index(self.notebook.select())
            self.notebook.forget(current_tab_index)  # Remove the tab from the notebook
            self.tabs.pop(current_tab_index)  # Remove the tab's text widget from the list
        else:
            messagebox.showwarning("Warning", "You must have at least one tab open.")
            
    def highlight_active_tab(self):
        """Apply syntax highlighting to the current tab."""
        self.textwidget = self.get_current_textwidget()
        SyntaxHighlite(self.textwidget).highlight_syntax()

    def get_current_textwidget(self):
        """Returns the ScrolledText widget of the currently selected tab."""
        current_tab_index = self.notebook.index(self.notebook.select())
        return self.tabs[current_tab_index]

    def openfile(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Python Files", "*.py"),
                ("Text Files", "*.textwidget"),
                ("All Files", "*.*"),
            ]
        )
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.textwidget = self.get_current_textwidget()
            self.textwidget.delete(1.0, tk.END)
            self.textwidget.insert(tk.END, content)
            self.notebook.tab(self.notebook.select(), text=file_path.split("/")[-1])
            self.add_to_history(file_path)
    def save_file_as(self, event=None):
        input_file_name = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[
                ("Python Files", "*.py"),
                ("Text Documents", "*.textwidget"),
                ("All Files", "*.*"),
            ],
        )
        if input_file_name:
            self.file_name = input_file_name
            self.write_to_file(self.file_name)
            self.add_to_history(self.file_name)
            self.root.title(
                "{} - {}".format(os.path.basename(self.file_name), self.program_name)
            )
        return "break"

    def savefile(self):
        self.textwidget = self.get_current_textwidget()
        content = self.textwidget.get(1.0, tk.END).strip()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".textwidget",
            filetypes=[("Python Files", "*.py"), ("Text Files", "*.textwidget")],
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            self.notebook.tab(self.notebook.select(), text=file_path.split("/")[-1])
            self.add_to_history(file_path)
    def write_to_file(self, file_name):
        try:
            content = self.textwidget.get(1.0, "end")
            with open(file_name, "w") as the_file:
                the_file.write(content)
        except IOError as io:
            messagebox.showerror("showerror", f"{io}")

    def move_to_next_tab(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        if current_tab_index < len(self.tabs) - 1:
            self.textwidget = self.get_current_textwidget()
            content = self.textwidget.get(1.0, tk.END).strip()
            next_tab_index = current_tab_index + 1
            self.notebook.select(next_tab_index)
            next_textwidget = self.tabs[next_tab_index]
            next_textwidget.insert(tk.END, content)
            self.textwidget.delete(1.0, tk.END)

    def move_to_previous_tab(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        if current_tab_index > 0:
            self.textwidget = self.get_current_textwidget()
            content = self.textwidget.get(1.0, tk.END).strip()
            prev_tab_index = current_tab_index - 1
            self.notebook.select(prev_tab_index)
            prev_textwidget = self.tabs[prev_tab_index]
            prev_textwidget.insert(tk.END, content)
            self.textwidget.delete(1.0, tk.END)

    def copy_to_next_tab(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        if current_tab_index < len(self.tabs) - 1:
            self.textwidget = self.get_current_textwidget()
            content = self.textwidget.get(1.0, tk.END).strip()
            next_tab_index = current_tab_index + 1
            next_textwidget = self.tabs[next_tab_index]
            next_textwidget.insert(tk.END, content)

    def add_to_history(self, file_path):
        if file_path in self.file_history:
            self.file_history.remove(file_path)
        self.file_history.insert(0, file_path)
        self.file_history = self.file_history[:10]
        self.savefile_history()
        self.update_recent_menu()

    def update_recent_menu(self):
        self.recent_menu.delete(0, tk.END)
        for file_path in self.file_history:
            self.recent_menu.add_command(
                label=file_path,
                command=lambda path=file_path: self.open_recent_file(path),
            )

    def open_recent_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            # Assuming you have a Text widget
            self.textwidget.delete("1.0", tk.END)  # Clear existing content
            self.textwidget.insert("1.0", content)  # Load file content
            print(f"Opened recent file: {file_path}")
        else:
            print(f"File not found: {file_path}")

    def load_file_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    if os.path.getsize(self.history_file) > 0:
                        return json.load(f)
            except json.JSONDecodeError:
                print("History file is corrupted. Resetting history.")
                return []
        return []

    def savefile_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.file_history, f)

    def readlines(self, event=None):
        input_file_name = filedialog.askopenfilename(
            defaultextension=".textwidget",
            filetypes=[
                ("All Files", "*.*"),
                ("Python Files", "*.py"),
                ("Text Documents", "*.textwidget"),
            ],
        )
        if input_file_name:
            self.file_name = input_file_name
            self.root.title(
                "{} - {}".format(os.path.basename(self.file_name), self.program_name)
            )
            self.textwidget.delete(1.0, tk.END)
            with open(self.file_name) as f:
                self.textwidget.insert(1.0, f.readlines())

    def save_incremented_version(self):
        if not self.file_name:
            # Automatically generate a default filename if none exists
            default_name = f"UntitledV1.textwidget"
            self.file_name = default_name

        # Get the directory and file name components
        directory = (
            os.path.dirname(self.file_name) or os.getcwd()
        )  # Default to the current working directory
        base_name = os.path.basename(self.file_name)
        name, ext = os.path.splitext(base_name)

        # Regular expression to find version suffix (e.g., V1, V2, etc.)
        version_pattern = r"^(.*?)(V\d+)?$"
        match = re.match(version_pattern, name)

        if match:
            base_name = match.group(1)
            existing_version = match.group(2)
            next_version = (
                f"V1" if not existing_version else f"V{int(existing_version[1:]) + 1}"
            )
        else:
            base_name = name
            next_version = "V1"

        # Create the new file name
        new_file_name = f"{base_name}{next_version}{ext}"
        new_file_path = os.path.join(directory, new_file_name)

        # Save the content to the new file
        try:
            content = self.textwidget.get(1.0, "end-1c")
            with open(new_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("File Saved", f"File saved as {new_file_name}")
            self.file_name = (
                new_file_path  # Update the file_name to the latest saved version
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")

    def run_file(self):
        """Run the current .py file in a new Python interpreter."""
        if not self.file_name:
            messagebox.showwarning("No File", "Save your file before running.")
            self.save_file_as()
            return

        # Check if the file is a Python file
        if not self.file_name.endswith(".py"):
            messagebox.showwarning(
                "Invalid File", "Only Python (.py) files can be executed."
            )
            return

        # Save the current file before executing
        self.savefile()

        # Run the file using subprocess
        try:
            process = subprocess.Popen(
                [
                    "python3",
                    self.file_name,
                ],  # Use "python" on Windows if "python3" is not available
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate()

            # Display output in a new window
            self.show_execution_output(stdout, stderr)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while running the file: {str(e)}"
            )

    def run_py_file(self):
        """Run the current .py file using runpy."""
        if not self.file_name:
            messagebox.showwarning("No File", "Save your file before running.")
            self.savefile()
            return

        # Check if the file is a Python file
        if not self.file_name.endswith(".py"):
            messagebox.showwarning(
                "Invalid File", "Only Python (.py) files can be executed."
            )
            return

        # Save the current file before executing
        self.savefile()

        try:
            # Redirect stdout and stderr to capture output
            import io
            import contextlib

            stdout = io.StringIO()
            stderr = io.StringIO()

            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                runpy.run_path(self.file_name, run_name="__main__")

            # Show output
            self.show_execution_output(stdout.getvalue(), stderr.getvalue())
        except Exception as e:
            self.show_execution_output("", f"Error occurred: {e}")

    def show_execution_output(self, stdout, stderr):
        """Display the output of the executed file in a new window."""
        output_window = tk.Toplevel(self.root)
        output_window.title("Execution Output")
        output_window.geometry("800x600")

        # Create a Text widget to display the output
        output_text = ScrolledText(output_window, wrap="word", font=("Consolas", 12))
        output_text.pack(fill="both", expand=True)

        # Insert stdout and stderr into the Text widget
        if stdout:
            output_text.insert("1.0", "=== Standard Output ===\n")
            output_text.insert("end", stdout)
        if stderr:
            output_text.insert("end", "\n=== Standard Error ===\n")
            output_text.insert("end", stderr)

        # Make the output read-only
        output_text.config(state="disabled")
        font(self.root)
        font_choice.grab_set()
        self.root.wait_window(font_choice)

    def cut(self):
        textwidget = self.get_current_textwidget()
        textwidget.event_generate("<<Cut>>")

    def copy(self):
        textwidget = self.get_current_textwidget()
        textwidget.event_generate("<<Copy>>")

    def paste(self):
        textwidget = self.get_current_textwidget()
        textwidget.event_generate("<<Paste>>")

    def undo(self):
        textwidget = self.get_current_textwidget()
        textwidget.event_generate("<<Undo>>")

    def redo(self, event=None):
        textwidget = self.get_current_textwidget()
        textwidget.event_generate("<<Redo>>")
        return "break"

    def search_output(self):
        self.top = tk.Toplevel()
        neddle_in_haystack = SearchText(self.top, self.textwidget)

    def find_replace(self, event=None):
        FindReplace(self.textwidget)

    def select_all(self, event=None):
        self.textwidget.tag_add("sel", "1.0", "end")
        return "break"

    def clear_clipboard(self):
        pyperclip.copy("")
        print("Clipboard cleared.")

    def comment_out_selected(self):
        try:
            start_index = self.textwidget.index("sel.first")
            end_index = self.textwidget.index("sel.last")
            selected_text = self.textwidget.get(start_index, end_index)

            # Prepend '#' to each line in the selection
            commented_text = "\n".join(
                f"# {line}" if not line.strip().startswith("#") else line
                for line in selected_text.split("\n")
            )
            self.textwidget.delete(start_index, end_index)
            self.textwidget.insert(start_index, commented_text)
        except tk.TclError:
            messagebox.showinfo("No Selection", "Please select text to comment out.")

    def remove_standalone_comments(self):
        try:
            # Get the entire text from the text widget
            full_text = self.textwidget.get("1.0", "end-1c")

            # Use a regular expression to remove lines starting with `#` (ignoring leading whitespace)
            uncommented_text = "\n".join(
                line
                for line in full_text.split("\n")
                if not line.strip().startswith("#")
            )

            # Replace the content of the text widget with the uncommented text
            self.textwidget.delete("1.0", "end")
            self.textwidget.insert("1.0", uncommented_text)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while removing comments: {str(e)}"
            )

    def remove_comments(self):
        try:
            # Get the entire text from the text widget
            full_text = self.textwidget.get("1.0", "end-1c")
            uncommented_text = "\n".join(
                line
                for line in full_text.split("\n")
                if not line.strip().startswith("#")
            )

            # Replace the content of the text widget with the uncommented text
            self.textwidget.delete("1.0", "end")
            self.textwidget.insert("1.0", uncommented_text)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while removing comments: {str(e)}"
            )

    def remove_text_between_quotes(self, quote_type="all"):
        try:
            # Get the full content of the text widget
            full_text = self.textwidget.get("1.0", "end-1c")

            # Define patterns for single, double, and triple quotes
            patterns = {
                "single": r"'[^']*'",
                "double": r'"[^"]*"',
                "triple": r'"""[\s\S]*?"""',
            }

            # Combine patterns based on the user's choice
            if quote_type == "single":
                regex = patterns["single"]
            elif quote_type == "double":
                regex = patterns["double"]
            elif quote_type == "triple":
                regex = patterns["triple"]
            else:  # Default to all
                regex = (
                    f"{patterns['triple']}|{patterns['single']}|{patterns['double']}"
                )

            # Remove matches using the regex
            updated_text = re.sub(regex, "", full_text)

            # Replace the content in the text widget
            self.textwidget.delete("1.0", "end")
            self.textwidget.insert("1.0", updated_text)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while removing text between quotes: {str(e)}",
            )

    def highlight_line(self, interval=100):
        self.textwidget.tag_remove("active_line", 1.0, "end")
        self.textwidget.tag_add("active_line", "insert linestart", "insert lineend+1c")
        self.textwidget.after(interval, self.toggle_highlight)

    def undo_highlight(self):
        self.textwidget.tag_remove("active_line", 1.0, "end")

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

    def highlight_section(self, event=None):
        try:
            if self.textwidget.tag_ranges("sel"):
                self.textwidget.tag_add("highlight", "sel.first", "sel.last")
                self.textwidget.tag_config("highlight", background="light yellow")
            else:
                messagebox.showinfo(
                    "No Selection", "Please select some text to highlight."
                )
        except tk.TclError as ex:
            print(ex)

    def syntax(self):
        if self.syn.get():
            SyntaxHighlite(self.textwidget)

    def textwidget_info(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        current_tab = self.notebook.nametowidget(
            self.notebook.tabs()[current_tab_index]
        )
        current_textwidget = self.get_current_textwidget()

        # Label for info in the current tab
        info_label = tk.Label(
            current_tab,
            text="Lines: 0  \n | Words: 0   \n| Characters: 0 \n| Cursor Position: Line 1   , Column 0",
        )
        info_label.grid(row=30, column=4)

        # Bind to text change and cursor movement events
        current_textwidget.bind("<KeyRelease>", self.update_info)
        current_textwidget.bind("<ButtonRelease-1>", self.update_info)
        current_textwidget.bind("<<Modified>>", self.on_text_modified)
        current_textwidget.bind("<ButtonRelease-2>", self.update_info)

    def on_text_modified(self, event):
        if self.textwidget.edit_modified():
            self.update_info(event)
            self.textwidget.edit_modified(False)

    def update_info(self, event=None):
        current_textwidget = self.get_current_textwidget()
        current_tab_index = self.notebook.index(self.notebook.select())
        current_tab = self.notebook.nametowidget(
            self.notebook.tabs()[current_tab_index]
        )
        info_label = current_tab.winfo_children()[
            -1
        ]  # Assuming the last widget is the info label

        # Get the current text content
        content = current_textwidget.get("1.0", "end-1c")

        # Count the lines, words, and characters
        lines = current_textwidget.index("end-1c").split(".")[0]
        words = len(content.split())
        characters = len(content)

        # Get the current cursor position (line and column)
        cursor_position = current_textwidget.index("insert")
        cursor_line, cursor_column = cursor_position.split(".")

        # Update the label with the new information
        info_label.config(
            text=f"Lines: {lines}   \n| Words: {words}       \n| Characters: {characters}     \n | Cursor Position: Line {cursor_line}, Column {cursor_column}"
        )

    def change_bg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.textwidget.config(bg=hexstr)

    def change_fg(self):
        (triple, hexstr) = askcolor()

        if hexstr:
            self.textwidget.config(fg=hexstr)

    def align_left(self, textwidget):
        self.textwidget = textwidget
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("left", justify=tk.LEFT)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "left")

    def align_center(self, textwidget):
        self.textwidget = textwidget
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("center", justify=tk.CENTER)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "center")

    def align_right(self, textwidget):
        self.textwidget = textwidget
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("right", justify=tk.RIGHT)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "right")

    def choose_font(self):
        FontBar(self.root, self.textwidget)

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
                italic_font = tk.font.Font(
                    self.textwidget, self.textwidget.cget("font")
                )
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
                underline_font = tk.font.Font(
                    self.textwidget, self.textwidget.cget("font")
                )
                underline_font.configure(underline=1)
                self.textwidget.tag_configure("underline", font=underline_font)
        except tk.TclError as ex:
            print(ex)

    def toggle_highlight(self, event=None):
        val = self.hltln.get()
        self.undo_highlight() if not val else self.highlight_line()

    def dedent(self, textwidget):
        try:
            selected_text = textwidget.get("sel.first", "sel.last")
            if selected_text:
                # Remove four spaces from the beginning of each line if present
                dedented_text = "\n".join(
                    line[4:] if line.startswith("    ") else line
                    for line in selected_text.split("\n")
                )
                textwidget.replace("sel.first", "sel.last", dedented_text)
        except Exception as e:
            print(e)

    def move_imports_to_top(self):
        try:
            # Get the entire text from the editor
            full_text = self.textwidget.get("1.0", "end-1c")

            # Split the content into lines and find all import statements
            lines = full_text.split("\n")
            import_lines = [
                line
                for line in lines
                if line.strip().startswith("import") or line.strip().startswith("from")
            ]

            # Remove import lines from the original content
            non_import_lines = [line for line in lines if line not in import_lines]

            # Combine import lines at the top followed by the remaining content
            new_content = "\n".join(import_lines + [""] + non_import_lines)

            # Replace the content in the text widget
            self.textwidget.delete("1.0", "end")
            self.textwidget.insert("1.0", new_content)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while moving imports: {str(e)}"
            )

    def remove_text_between_quotes(self, quote_type="all"):
        try:
            # Get the full content of the text widget
            full_text = self.textwidget.get("1.0", "end-1c")

            # Define patterns for single, double, and triple quotes
            patterns = {
                "single": r"'[^']*'",
                "double": r'"[^"]*"',
                "triple": r'"""[\s\S]*?"""',
            }

            # Combine patterns based on the user's choice
            if quote_type == "single":
                regex = patterns["single"]
            elif quote_type == "double":
                regex = patterns["double"]
            elif quote_type == "triple":
                regex = patterns["triple"]
            else:  # Default to all
                regex = (
                    f"{patterns['triple']}|{patterns['single']}|{patterns['double']}"
                )

            # Remove matches using the regex
            updated_text = re.sub(regex, "", full_text)

            # Replace the content in the text widget
            self.textwidget.delete("1.0", "end")
            self.textwidget.insert("1.0", updated_text)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while removing text between quotes: {str(e)}",
            )

    def insert_selfs(self, textwidget):
        try:
            start_index = self.textwidget.index("sel.first")
            end_index = self.textwidget.index("sel.last")
            selected_text = self.textwidget.get(start_index, end_index)

            if not selected_text.strip():
                messagebox.showinfo("No Selection", "Please select a function or text.")
                return

            new_lines = [
                f"self.{line.strip()}"
                if line.strip() and not line.strip().startswith("self.")
                else line
                for line in selected_text.split("\n")
            ]
            new_text = "\n".join(new_lines)
            self.textwidget.delete(start_index, end_index)
            self.textwidget.insert(start_index, new_text)
        except tk.TclError:
            messagebox.showinfo("Error", "Please select text to modify.")

    def in_entire_text(self, textwidget):
        self.textwidget = textwidget
        # Get the entire content of the text widget
        full_text = self.textwidget.get("1.0", "end-1c")
        new_lines = []

        # Regex to match function definitions
        func_def_pattern = r"^(def\s+\w+\()([^)]*)\):"

        for line in full_text.split("\n"):
            match = re.match(func_def_pattern, line.strip())
            if match:
                func_name = match.group(1)  # "def function_name("
                args = match.group(2)  # Current arguments (empty or not)
                # Add 'self' if it's not already present
                if "self" not in args.split(","):
                    args = "self" if not args else f"self, {args}"
                new_line = f"{func_name}{args}):"
            else:
                new_line = line  # Leave other lines unchanged
            new_lines.append(new_line)

        # Join modified lines and update the text widget
        new_text = "\n".join(new_lines)
        self.textwidget.delete("1.0", "end")
        self.textwidget.insert("1.0", new_text)

    def in_parentheses(self, textwidget):
        self.textwidget = textwidget
        try:
            start_index = self.textwidget.index("sel.first")
            end_index = self.textwidget.index("sel.last")
        except Exception:
            return  # Do nothing if no selection

        # Get the selected text
        selected_text = self.textwidget.get(start_index, end_index)
        new_lines = []

        # Regex to match function definitions
        func_def_pattern = r"^(def\s+\w+\()([^)]*)\):"

        for line in selected_text.split("\n"):
            match = re.match(func_def_pattern, line.strip())
            if match:
                func_name = match.group(1)  # "def function_name("
                args = match.group(2)  # Current arguments (empty or not)
                # Add 'self' if it's not already present
                if "self" not in args.split(","):
                    args = "self" if not args else f"self, {args}"
                new_line = f"{func_name}{args}):"
            else:
                new_line = line  # Leave other lines unchanged
            new_lines.append(new_line)

        # Join modified lines and update the text widget
        new_text = "\n".join(new_lines)
        self.textwidget.delete(start_index, end_index)
        self.textwidget.insert(start_index, new_text)

    def move_imports_to_top(self):
        try:
            # Get the entire text from the editor
            full_text = self.textwidget.get("1.0", "end-1c")

            # Split the content into lines and find all import statements
            lines = full_text.split("\n")
            import_lines = [
                line
                for line in lines
                if line.strip().startswith("import") or line.strip().startswith("from")
            ]

            # Remove import lines from the original content
            non_import_lines = [line for line in lines if line not in import_lines]

            # Combine import lines at the top followed by the remaining content
            new_content = "\n".join(import_lines + [""] + non_import_lines)

            # Replace the content in the text widget
            self.textwidget.delete("1.0", "end")
            self.textwidget.insert("1.0", new_content)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while moving imports: {str(e)}"
            )

    def show_color_selector(self):
        self.tab = ttk.Frame(self.notebook)
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.tab, text=f"self.tab {len(self.tabs) + 1}")
        self.color_select_menu = ColorClipboardApp(self.tab)
        self.tabs.append(self.color_select_menu)
        self.notebook.select(len(self.tabs) - 1)

    def at_cursor(self, textwidget):
        top = tk.Toplevel()
        self.entry = tk.Entry(top, bd=8, bg="wheat")
        self.entry.grid(row=0, column=0)
        self.textwidget = textwidget

    def submit():
        word = self.entry.get()
        self.textwidget.insert(tk.INSERT, word)

        btn = tk.Button(top, bd=3, bg="light green", command=submit)
        btn.grid(row=3, column=1)

    def help(self):
        help1 = """
        PyEditor Help
        -------------
        Welcome to PyEditor! Here's a quick
        guide to using the application:

        File Menu:
        - New: Create a new file (Ctrl+N).
        - Open: Open an existing file (Ctrl+O).
        - Save: Save the current file (Ctrl+S).
        - Save As: Save the file with
        a new name or type (Shift+Ctrl+S).
        - Save Version: Save a new version
        of the file incrementally.
        - Recently Loaded: Access the
        most recently opened files.
        - Run File: Run the current
        Python file (F10).
        - Exit: Quit the application (Alt+F4)."""
        help2 = """
        Edit Menu:
        - Cut, Copy, Paste:
        Standard editing actions (Ctrl+X, Ctrl+C, Ctrl+V).
        - Undo/Redo: Undo or redo changes (Ctrl+Z, Ctrl+Y).
        - Find/Replace: Find and replace text in the editor (Ctrl+F).
        - Highlight Section:
          Highlight selected text.
        - Indent/Dedent:
          Adjust indentation (Ctrl+]/Ctrl+[).
        - Comment/Uncomment: Comment or remove comments from code."""
        help3 = """ 
        View Menu:
        - Highlight Current Line:
        Toggle line highlighting.
        - Syntax Highlighting:
        Enable or disable syntax highlighting.

        Custom Menu:
        - Insert selfs:
        Convert functions to methods by adding `self`.
        - Move Imports to Top:
        Organize imports at the top of the file.
        - Remove Text Between Quotes:
        Remove specific or all quoted text."""
        help4 = """
        Formatting:
        - Bold, Italic, Underline:
        Style selected text.
        - Choose Font:
        Change the font and size.

        Additional Features:
        - File Explorer: Browse directories and open files.
        - Syntax Highlighting: Real-time highlighting of Python code.
        - Incremental Save: Save versions of your file with versioning.
        - Execution Output: Run Python scripts and view the output."""
        help5 = """
        Shortcuts:
        - Ctrl+A: Select all text.
        - Ctrl+/ or Ctrl+Bracket: Comment/Indent lines.
        - Ctrl+Shift+S: Save As.

        Themes:
        - Change background and foreground colors or choose from predefined themes.

        For more assistance, visit the documentation or contact support.
        """
        messagebox.showinfo("Help", help1)
        messagebox.showinfo("Help", help2)
        messagebox.showinfo("Help", help3)
        messagebox.showinfo("Help", help4)
        messagebox.showinfo("Help", help5)

    def about(self):
        about_str = """
        This is a Custom Pycode Editor Application
            John Hewitt rev1 Jan 2025"""
        messagebox.showinfo("About", about_str)
    ####################CODE FORMATTER##################################################
##    def open_format(self):
##        """Retrieve the active Text widget and open the formatter tab."""
##        current_tab = self.notebook.select()
##        current_tab_frame = self.notebook.nametowidget(current_tab)
##        textwidgets = [child for child in current_tab_frame.winfo_children() if isinstance(child, tk.Text)]
##        
##        if not textwidgets:
##            messagebox.showerror("Error", "No Text widget found in the current tab!")
##            return
##        
##        textwidget = textwidgets[0]  # Assuming the first Text widget is the one we want
##        self.open_formatter_tab(textwidget)


    def open_formatter_tab(self, textwidget):
        """Open the Code Formatter as a new tab."""
        # Ensure the passed widget is a Text widget
        if not isinstance(textwidget, tk.Text):
            messagebox.showerror("Error", "Provided widget is not a Text widget!")
            return
        
        # Create a new tab for the formatter
        formatter_tab = ttk.Frame(self.notebook)
        self.notebook.add(formatter_tab, text="Code Formatter")
        self.notebook.select(formatter_tab)  # Switch to the formatter tab

        # Initialize CodeFormatterApp in the new tab
        code = textwidget.get("1.0", tk.END).strip()
        formatter_app = CodeFormatterApp(formatter_tab,self.textwidget)
      
    
    ############################ADD####ON#####DIRECTORY####BROWSER############
    def filelist(self, path):
        self.top = Toplevel()
        self.path = path
        self.top.attributes("-topmost", True)  # Keeps the window on top
        self.path_var = tk.StringVar()
        self.dir_path = tk.Entry(
            self.top, bd=6, bg="wheat", textvariable=self.path_var, width=150
        )
        self.dir_path.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.dir_path.insert(0, os.getcwd())

        # Treeview for directory browsing
        self.tree_frame = tk.Frame(self.top)
        self.tree_frame.grid(row=1, column=1, sticky="nsew")
        self.treeview = ttk.Treeview(
            self.tree_frame, columns=("filename", "size", "modified"), show="headings"
        )
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        self.treeview.heading("filename", text="Filename")
        self.treeview.column("filename", width=200)
        self.treeview.heading("size", text="Size")
        self.treeview.column("size", width=100)
        self.treeview.heading("modified", text="Modified")
        self.treeview.column("modified", width=150)

        # Scrollbar for Treeview
        self.tree_scr = tk.Scrollbar(
            self.tree_frame, orient="vertical", command=self.treeview.yview
        )
        self.tree_scr.grid(row=0, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=self.tree_scr.set)
        self.bt1 = ttk.Button(
            self.top,text="Directory", command=self.makedirlist
        )
        self.bt1.grid(row=3, column=1)
        self.bt2 = tk.Button(
            self.top,
            bd=8,
            bg="gold2",
            text="get file recursively",
            command=self.recursive_new_list,
        )
        self.bt2.grid(row=4, column=1)
        self.bt3 = tk.Button(
            self.top,
            bd=8,
            bg="dark turquoise",
            text="New_Directory",
            command=self.newdirlist,
        )
        self.bt3.grid(row=5, column=1)
        self.top.grid_columnconfigure(2, weight=1)

    def on_treeview_select(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            file_name = self.treeview.item(selected_item[0])["values"][0]
            file_path = os.path.join(self.path, file_name)

        self.showcontent(file_path)

    def add_file_to_treeview(self, root, file):
        item_path = os.path.join(root, file)  # Full path to the item
        file_size = os.path.getsize(item_path)  # Get file size
        modified_timestamp = os.path.getmtime(item_path)  # Get last modified timestamp
        modified_date = datetime.fromtimestamp(modified_timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )  # Format timestamp

        # Insert the file information into the Treeview
        self.treeview.insert("", "end", values=(item_path, file_size, modified_date))

    def listing(self):
        self.flist = os.listdir(self.path)
        self.treeview.delete(*self.treeview.get_children())
        for item in self.flist:
            if item.endswith((".py", ".textwidget")):
                file_size = os.path.getsize(item)
                modified_timestamp = os.path.getmtime(item)
                modified_date = datetime.fromtimestamp(modified_timestamp).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                self.treeview.insert("", "end", values=(item, file_size, modified_date))
        self.path = os.getcwd()

    def recursive_new_list(self):
        self.path = filedialog.askdirectory()
        if self.path:  # Check if a directory was selected
            os.chdir(self.path)
            self.dir_path.insert(tk.END, self.path)
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith((".py", ".textwidget")):
                    self.add_file_to_treeview(root, file)

    def makedirlist(self):
        self.path = os.getcwd()
        self.listing()

    def newdirlist(self):
        self.path = filedialog.askdirectory()
        if self.path:  # Check if a directory was selected
            os.chdir(self.path)
            self.dir_path.insert(tk.END, self.path)
            self.listing()

    def showcontent(self, event=None):
        selected_item = self.treeview.selection()
        if selected_item:
            file_name = self.treeview.item(selected_item[0])["values"][0]
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

    def sort_treeview(self, col, reverse):
        # Fetching all children of the Treeview
        items = [
            (self.treeview.item(iid, "values"), iid)
            for iid in self.treeview.get_children("")
        ]

        # Sort the items based on the specified column
        items.sort(key=lambda k: k[0][col], reverse=reverse)

        # Rearrange items in the Treeview
        for index, (values, iid) in enumerate(items):
            self.treeview.move(iid, "", index)

        # Reverse sort next time
        self.treeview.heading(col, command=lambda: self.sort_treeview(col, not reverse))


###########################################################################


class FindReplace:
    def __init__(self, textwidget):
        self.textwidget = textwidget
        self.top = tk.Toplevel()
        self.top.title("Find & Replace")
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        self.use_regex = tk.BooleanVar()
        self.create_find_replace_interface()

    def create_find_replace_interface(self):
        tk.Label(self.top, text="Find:").grid(row=0, column=0, padx=4, pady=4)
        self.find_entry = tk.Entry(
            self.top, textvariable=self.find_var, width=20, background="cornsilk"
        )
        self.find_entry.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(self.top, text="Replace With:").grid(row=1, column=0, padx=4, pady=4)
        self.replace_entry = tk.Entry(
            self.top, textvariable=self.replace_var, width=20, background="seashell"
        )
        self.replace_entry.grid(row=1, column=1, padx=4, pady=4)

        tk.Checkbutton(self.top, text="Use Regex", variable=self.use_regex).grid(
            row=2, column=0, columnspan=2
        )

        find_btn = tk.Button(self.top, text="Find Next", command=self.find_text)
        find_btn.grid(row=3, column=0, padx=4, pady=4)

        replace_btn = tk.Button(self.top, text="Replace", command=self.replace_text)
        replace_btn.grid(row=3, column=1, padx=4, pady=4)

        replace_all_btn = tk.Button(
            self.top, text="Replace All", command=self.replace_all_text
        )
        replace_all_btn.grid(row=4, column=1, padx=4, pady=4)

        regex_help_btn = tk.Button(self.top, text="Regex Help", command=self.regex_help)
        regex_help_btn.grid(row=5, column=0, columnspan=2, pady=4)

        self.find_entry.focus_set()
        self.find_entry.bind("<Return>", lambda event: self.find_text())
        self.replace_entry.bind("<Return>", lambda event: self.replace_text())

    def regex_help(self):
        help_text = """
        Common Regex Patterns:
        - ^abc: Matches any string that starts with "abc"
        - abc$: Matches any string that ends with "abc"
        - [a-zA-Z]: Matches any single letter
        - \\d: Matches any digit
        - .*: Matches any character (except for newline characters)
        - ab|cd: Matches "ab" or "cd"
        """
        messagebox.showinfo("Regex Help", help_text)

    def find_text(self):
        self.textwidget.tag_remove("found", "1.0", tk.END)
        search_query = self.find_var.get()
        if search_query:
            content = self.textwidget.get("1.0", tk.END)
            idx = "1.0"
            last_idx = None
            try:
                if self.use_regex.get():
                    for match in re.finditer(search_query, content):
                        start, end = match.start(), match.end()
                        start_idx = self.textwidget.index(f"{idx}+{start}c")
                        end_idx = self.textwidget.index(f"{idx}+{end}c")
                        self.textwidget.tag_add("found", start_idx, end_idx)
                        last_idx = start_idx
                else:
                    while True:
                        idx = self.textwidget.search(
                            search_query, idx, nocase=1, stopindex=tk.END
                        )
                        if not idx:
                            break
                        last_idx = idx
                        lastidx = f"{idx}+{len(search_query)}c"
                        self.textwidget.tag_add("found", idx, lastidx)
                        idx = f"{lastidx}+1c"

                if last_idx:
                    self.textwidget.tag_config(
                        "found", background="purple", foreground="yellow"
                    )
                    self.textwidget.see(last_idx)
                    self.textwidget.mark_set("insert", last_idx)
                    self.textwidget.focus()
            except re.error as e:
                messagebox.showerror("Regex Error", str(e))

    def replace_text(self):
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        if not find_text or not replace_text:
            return
        self.textwidget.tag_remove("found", "1.0", tk.END)
        content = self.textwidget.get("1.0", tk.END)
        if self.use_regex.get():
            try:
                replaced_content, count = re.subn(find_text, replace_text, content)
                if count > 0:
                    self.textwidget.delete("1.0", tk.END)
                    self.textwidget.insert("1.0", replaced_content)
            except re.error as e:
                messagebox.showerror("Regex Error", str(e))
        else:
            if find_text in content:
                replaced_content = content.replace(find_text, replace_text)
                self.textwidget.delete("1.0", tk.END)
                self.textwidget.insert("1.0", replaced_content)

    def replace_all_text(self):
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        if not find_text or not replace_text:
            return
        self.textwidget.tag_remove("found", "1.0", tk.END)
        try:
            if self.use_regex.get():
                content = self.textwidget.get("1.0", tk.END)
                replaced_content, _ = re.subn(find_text, replace_text)
                self.textwidget.delete("1.0", tk.END)
                self.textwidget.insert("1.0", replaced_content)
            else:
                content = self.textwidget.get("1.0", tk.END)
                replaced_content = content.replace(find_text, replace_text)
                self.textwidget.delete("1.0", tk.END)
                self.textwidget.insert("1.0", replaced_content)
        except re.error as e:
            messagebox.showerror("Regex Error", str(e))
####|(\"\"\"[\s\S]*?\"\"\"|\"\"\"[\s\S]*?\"\"\")"
##################################################################################
class SyntaxHighlite:
    def __init__(self, textwidget):
        textwidget
        self.syntax_elements = {
            "comment": r"#[^\n]*",
            "number": r"\b\d+(\.\d+)?\b",
            "string": r".? |\".*?\"",
            "docstring" : r"\b '''.*?'''\b",
            'docstring2': r'\b """*?"""\b;',
            "keyword": r"\b(import|as|pass|return|def|if|else|elif|yield|for|while|break|continue|try|except|finally|with|as|in|not|and|or|is|None|True|False)\b",
            "classes": r"\b(@static_method|class|@property|@class_method|super|cls)\b",
            "selfs": r"\b(self)\b",
        }
        self.configure_tags()

        # Trigger syntax highlighting after any key is pressed
        self.textwidget.bind("<KeyRelease>", self.highlight_syntax)

    def configure_tags(self):
        self.textwidget.tag_config("keyword", foreground="DarkOrange3")
        self.textwidget.tag_config("string", foreground="turquoise4")
        self.textwidget.tag_config("comment", foreground="firebrick4")
        self.textwidget.tag_config("number", foreground="gold3")
        self.textwidget.tab_config("selfs", foreground="MediumOrchid4")
        self.textwidget.tag_config("classes", foreground="DeepSkyBlue3")
        self.textwidget.tag_config("docstring", background="light yellow",foreground="SpringGreen2")
        self.textwidget.tag_config("docstring2", foreground="SpringGreen2")

    def highlight_syntax(self, event=None):
        for tag in list(self.syntax_elements.keys()):
            self.textwidget.tag_remove(tag, "1.0", tk.END)

        for tag, pattern in list(self.syntax_elements.items()):
            start_index = "1.0"
            while True:
                match = re.search(
                    pattern, self.textwidget.get(start_index, tk.END), re.MULTILINE
                )
                if not match:
                    break
                start_index = self.textwidget.index(f"{start_index}+{match.start()}c")
                end_index = self.textwidget.index(
                    f"{start_index}+{match.end() - match.start()}c"
                )
                self.textwidget.tag_add(tag, start_index, end_index)
                start_index = end_index


#################################################################################


class SearchText:
    def __init__(self, top, textwidget):
        self.top = top
        self.textwidget = textwidget
        # Label and Entry for search string
        tk.Label(top, text="Search Term:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.search_entry = tk.Entry(top, width=30)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        # Checkbutton for case sensitivity
        self.ignore_case_var = tk.BooleanVar(value=True)
        self.case_checkbox = tk.Checkbutton(
            top, text="Ignore Case", variable=self.ignore_case_var
        )
        self.case_checkbox.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        # Button to trigger search
        self.search_button = ttk.Button(top, text="Search", command=self.start_search)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create a Text widget for demonstration

        # Add sample text to the Text widget

    def start_search(self):
        # Get arguments from widgets
        needle = self.search_entry.get()
        if_ignore_case = self.ignore_case_var.get()

        # Create a Toplevel for search results
        search_top_level = tk.Toplevel(self.top)
        search_top_level.title("Search Output")
        search_box = tk.Entry(search_top_level, width=30)
        search_box.grid(row=0, column=0, padx=10, pady=5)

        # Perform search
        self.search_output(needle, if_ignore_case, search_top_level, search_box)

    def search_output(self, needle, if_ignore_case, search_top_level, search_box):
        # Remove previous matches
        self.textwidget.tag_remove("match", "1.0", tk.END)

        matches_found = 0
        if needle:
            start_pos = "1.0"
            while True:
                # Search for the needle
                start_pos = self.textwidget.search(
                    needle, start_pos, nocase=if_ignore_case, stopindex=tk.END
                )
                if not start_pos:
                    break

                # Highlight matches
                end_pos = f"{start_pos}+{len(needle)}c"
                self.textwidget.tag_add("match", start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos

            # Configure highlighting
            self.textwidget.tag_config("match", foreground="red", background="yellow")

        # Update the search output window
        search_top_level.title(f"{matches_found} matches found")
        search_box.delete(0, tk.END)
        search_box.insert(0, f"{matches_found} matches found")


class SyntaxHighlite:
    def __init__(self, textwidget):
        self.textwidget = textwidget
        self.syntax_elements = {
            "comment": r"#[^\n]*|(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\")",
            "number": r"\b\d+(\.\d+)?\b",
            "string": r'".*?"|\'.*?\'',
            "keyword": r"\b(import|as|pass|return|def|if|else|elif|for|while|break|continue|try|except|finally|with|as|in|not|and|or|is|None|True|False|yield)\b",
            "classes": r"\b(@static_method|class|@property|@class_method|self|super|cls)\b",
        }
        self.configure_tags()

        # Trigger syntax highlighting after any key is pressed
        self.textwidget.bind("<KeyRelease>", self.highlight_syntax)

    def configure_tags(self):
        self.textwidget.tag_config("keyword", foreground="sienna2")
        self.textwidget.tag_config("string", foreground="cyan")
        self.textwidget.tag_config("comment", foreground="red")
        self.textwidget.tag_config("number", foreground="lawngreen")
        self.textwidget.tag_config("classes", foreground="deep pink")

    def highlight_syntax(self, event=None):
        for tag in list(self.syntax_elements.keys()):
            self.textwidget.tag_remove(tag, "1.0", tk.END)

        for tag, pattern in list(self.syntax_elements.items()):
            start_index = "1.0"
            while True:
                match = re.search(
                    pattern, self.textwidget.get(start_index, tk.END), re.MULTILINE
                )
                if not match:
                    break
                start_index = self.textwidget.index(f"{start_index}+{match.start()}c")
                end_index = self.textwidget.index(
                    f"{start_index}+{match.end() - match.start()}c"
                )
                self.textwidget.tag_add(tag, start_index, end_index)
                start_index = end_index


################from tkinter.colorchooser import askcolor#################################################################
class ColorClipboardApp:
    def __init__(self, tab):
        self.tab = tab

        # List of colors
        self.all_colors = [
            "AntiqueWhite1",
            "AntiqueWhite2",
            "AntiqueWhite3",
            "AntiqueWhite4",
            "CadetBlue1",
            "CadetBlue2",
            "CadetBlue3",
            "CadetBlue4",
            "DarkGoldenrod1",
            "DarkGoldenrod2",
            "DarkGoldenrod3",
            "DarkGoldenrod4",
            "DarkOliveGreen1",
            "DarkOliveGreen2",
            "DarkOliveGreen3",
            "DarkOliveGreen4",
            "DarkOrange1",
            "DarkOrange2",
            "DarkOrange3",
            "DarkOrange4",
            "DarkOrchid1",
            "DarkOrchid2",
            "DarkOrchid3",
            "DarkOrchid4",
            "DarkSeaGreen1",
            "DarkSeaGreen2",
            "DarkSeaGreen3",
            "DarkSeaGreen4",
            "DarkSlateGray1",
            "DarkSlateGray2",
            "DarkSlateGray3",
            "DarkSlateGray4",
            "DeepPink2",
            "DeepPink3",
            "DeepPink4",
            "DeepSkyBlue2",
            "DeepSkyBlue3",
            "DeepSkyBlue4",
            "DodgerBlue2",
            "DodgerBlue3",
            "DodgerBlue4",
            "HotPink1",
            "HotPink2",
            "HotPink3",
            "HotPink4",
            "IndianRed1",
            "IndianRed2",
            "IndianRed3",
            "IndianRed4",
            "LavenderBlush2",
            "LavenderBlush3",
            "LavenderBlush4",
            "LemonChiffon2",
            "LemonChiffon3",
            "LemonChiffon4",
            "LightBlue1",
            "LightBlue2",
            "LightBlue3",
            "LightBlue4",
            "LightCyan2",
            "LightCyan3",
            "LightCyan4",
            "LightGoldenrod1",
            "LightGoldenrod2",
            "LightGoldenrod3",
            "LightGoldenrod4",
            "LightPink1",
            "LightPink2",
            "LightPink3",
            "LightPink4",
            "LightSalmon2",
            "LightSalmon3",
            "LightSalmon4",
            "LightSkyBlue1",
            "LightSkyBlue2",
            "LightSkyBlue3",
            "LightSkyBlue4",
            "LightSteelBlue1",
            "LightSteelBlue2",
            "LightSteelBlue3",
            "LightSteelBlue4",
            "LightYellow2",
            "LightYellow3",
            "LightYellow4",
            "MediumOrchid1",
            "MediumOrchid2",
            "MediumOrchid3",
            "MediumOrchid4",
            "MediumPurple1",
            "MediumPurple2",
            "MediumPurple3",
            "MediumPurple4",
            "MistyRose2",
            "MistyRose3",
            "MistyRose4",
            "NavajoWhite2",
            "NavajoWhite3",
            "NavajoWhite4",
            "OliveDrab1",
            "OliveDrab2",
            "OliveDrab4",
            "OrangeRed2",
            "OrangeRed3",
            "OrangeRed4",
            "PaleGreen1",
            "PaleGreen2",
            "PaleGreen3",
            "PaleGreen4",
            "PaleTurquoise1",
            "PaleTurquoise2",
            "PaleTurquoise3",
            "PaleTurquoise4",
            "PaleVioletRed1",
            "PaleVioletRed2",
            "PaleVioletRed3",
            "PaleVioletRed4",
            "PeachPuff2",
            "PeachPuff3",
            "PeachPuff4",
            "RosyBrown1",
            "RosyBrown2",
            "RosyBrown3",
            "RosyBrown4",
            "RoyalBlue1",
            "RoyalBlue2",
            "RoyalBlue3",
            "RoyalBlue4",
            "SeaGreen1",
            "SeaGreen2",
            "SeaGreen3",
            "SkyBlue1",
            "SkyBlue2",
            "SkyBlue3",
            "SkyBlue4",
            "SlateBlue1",
            "SlateBlue2",
            "SlateBlue3",
            "SlateBlue4",
            "SlateGray1",
            "SlateGray2",
            "SlateGray3",
            "SlateGray4",
            "SpringGreen2",
            "SpringGreen3",
            "SpringGreen4",
            "SteelBlue1",
            "SteelBlue2",
            "SteelBlue3",
            "SteelBlue4",
            "VioletRed1",
            "VioletRed2",
            "VioletRed3",
            "VioletRed4",
            "alice blue",
            "antique white",
            "aquamarine",
            "aquamarine2",
            "aquamarine4",
            "azure",
            "azure2",
            "azure3",
            "azure4",
            "bisque",
            "bisque2",
            "bisque3",
            "bisque4",
            "blanched almond",
            "blue",
            "blue violet",
            "blue2",
            "blue4",
            "brown1",
            "brown2",
            "brown3",
            "brown4",
            "burlywood1",
            "burlywood2",
            "burlywood3",
            "burlywood4",
            "cadet blue",
            "chartreuse2",
            "chartreuse3",
            "chartreuse4",
            "chocolate1",
            "chocolate2",
            "chocolate3",
            "coral",
            "coral1",
            "coral2",
            "coral3",
            "coral4",
            "cornflower blue",
            "cornsilk2",
            "cornsilk3",
            "cornsilk4",
            "cyan",
            "cyan2",
            "cyan3",
            "cyan4",
            "dark goldenrod",
            "dark green",
            "dark khaki",
            "dark olive green",
            "dark orange",
            "dark orchid",
            "dark salmon",
            "dark sea green",
            "dark slate blue",
            "dark slate gray",
            "dark turquoise",
            "dark violet",
            "deep pink",
            "deep sky blue",
            "dim gray",
            "dodger blue",
            "firebrick1",
            "firebrick2",
            "firebrick3",
            "firebrick4",
            "floral white",
            "forest green",
            "gainsboro",
            "ghost white",
            "gold",
            "gold2",
            "gold3",
            "gold4",
            "goldenrod",
            "goldenrod1",
            "goldenrod2",
            "goldenrod3",
            "goldenrod4",
            "gray",
            "gray1",
            "gray10",
            "gray11",
            "gray12",
            "gray13",
            "gray14",
            "gray15",
            "gray16",
            "gray17",
            "gray18",
            "gray19",
            "gray2",
            "gray20",
            "gray21",
            "gray22",
            "gray23",
            "gray24",
            "gray25",
            "gray26",
            "gray27",
            "gray28",
            "gray29",
            "gray3",
            "gray30",
            "gray31",
            "gray32",
            "gray33",
            "gray34",
            "gray35",
            "gray36",
            "gray37",
            "gray38",
            "gray39",
            "gray4",
            "gray40",
            "gray42",
            "gray43",
            "gray44",
            "gray45",
            "gray46",
            "gray47",
            "gray48",
            "gray49",
            "gray5",
            "gray50",
            "gray51",
            "gray52",
            "gray53",
            "gray54",
            "gray55",
            "gray56",
            "gray57",
            "gray58",
            "gray59",
            "gray6",
            "gray60",
            "gray61",
            "gray62",
            "gray63",
            "gray64",
            "gray65",
            "gray66",
            "gray67",
            "gray68",
            "gray69",
            "gray7",
            "gray70",
            "gray71",
            "gray72",
            "gray73",
            "gray74",
            "gray75",
            "gray76",
            "gray77",
            "gray78",
            "gray79",
            "gray8",
            "gray80",
            "gray81",
            "gray82",
            "gray83",
            "gray84",
            "gray85",
            "gray86",
            "gray87",
            "gray88",
            "gray89",
            "gray9",
            "gray90",
            "gray91",
            "gray92",
            "gray93",
            "gray94",
            "gray95",
            "gray97",
            "gray98",
            "gray99",
            "green yellow",
            "green2",
            "green3",
            "green4",
            "honeydew2",
            "honeydew3",
            "honeydew4",
            "hot pink",
            "indian red",
            "ivory2",
            "ivory3",
            "ivory4",
            "khaki",
            "khaki1",
            "khaki2",
            "khaki3",
            "khaki4",
            "lavender",
            "lavender blush",
            "lawn green",
            "lemon chiffon",
            "light blue",
            "light coral",
            "light cyan",
            "light goldenrod",
            "light goldenrod yellow",
            "light grey",
            "light pink",
            "light salmon",
            "light sea green",
            "light sky blue",
            "light slate blue",
            "light slate gray",
            "light steel blue",
            "light yellow",
            "lime green",
            "linen",
            "magenta2",
            "magenta3",
            "magenta4",
            "maroon",
            "maroon1",
            "maroon2",
            "maroon3",
            "maroon4",
            "medium aquamarine",
            "medium blue",
            "medium orchid",
            "medium purple",
            "medium sea green",
            "medium slate blue",
            "medium spring green",
            "medium turquoise",
            "medium violet red",
            "midnight blue",
            "mint cream",
            "misty rose",
            "navajo white",
            "navy",
            "old lace",
            "olive drab",
            "orange",
            "orange red",
            "orange2",
            "orange3",
            "orange4",
            "orchid1",
            "orchid2",
            "orchid3",
            "orchid4",
            "pale goldenrod",
            "pale green",
            "pale turquoise",
            "pale violet red",
            "papaya whip",
            "peach puff",
            "pink",
            "pink1",
            "pink2",
            "pink3",
            "pink4",
            "plum1",
            "plum2",
            "plum3",
            "plum4",
            "powder blue",
            "purple",
            "purple1",
            "purple2",
            "purple3",
            "purple4",
            "red",
            "red2",
            "red3",
            "red4",
            "rosy brown",
            "royal blue",
            "saddle brown",
            "salmon",
            "salmon1",
            "salmon2",
            "salmon3",
            "salmon4",
            "sandy brown",
            "sea green",
            "seashell2",
            "seashell3",
            "seashell4",
            "sienna1",
            "sienna2",
            "sienna3",
            "sienna4",
            "sky blue",
            "slate blue",
            "slate gray",
            "snow",
            "snow2",
            "snow3",
            "snow4",
            "spring green",
            "steel blue",
            "tan1",
            "tan2",
            "tan4",
            "thistle",
            "thistle1",
            "thistle2",
            "thistle3",
            "thistle4",
            "tomato",
            "tomato2",
            "tomato3",
            "tomato4",
            "turquoise",
            "turquoise1",
            "turquoise2",
            "turquoise3",
            "turquoise4",
            "violet red",
            "wheat1",
            "wheat2",
            "wheat3",
            "wheat4",
            "white smoke",
            "yellow",
            "yellow green",
            "yellow2",
            "yellow3",
            "yellow4",
        ]

        # Button display frame
        self.button_frame = tk.Frame(self.tab)
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        # Show colors as buttons
        self.display_colors()

    def display_colors(self):
        num_rows = 45  # Number of rows
        row, col = 0, 0

        for color in self.all_colors:
            # Create a button for each color
            button = tk.Button(
                self.button_frame,
                text=color,
                bg=color,
                font=("Arial", 9),
                command=lambda c=color: self.copy_to_clipboard(c),
            )
            button.grid(row=row, column=col, sticky="nsew")

            row += 1
            if row >= num_rows:
                row = 0
                col += 1

        # Configure grid weights for resizing
        for i in range(num_rows):
            self.button_frame.rowconfigure(i, weight=1)
        for j in range(col + 1):
            self.button_frame.columnconfigure(j, weight=1)

    def copy_to_clipboard(self, color_name):
        """Copy the selected color name to clipboard."""
        self.tab.clipboard_clear()
        self.tab.clipboard_append(color_name)
        self.tab.update()
        print(f"Copied '{color_name}' to clipboard!")


#################################################################################


class FontBar:
    def __init__(self, parent, textwidget):
        self.parent = parent
        self.textwidget = textwidget
        self.top = tk.Toplevel(parent)
        self.top.title("Font Selector")
        self.top.geometry("500x600")
        self.font = font.Font(
            font=self.textwidget.cget("font")
        )  # Use the current font of the text widget

        # Listbox for font families
        tk.Label(self.top, text="Select Font Family:").pack()
        self.font_listbox = tk.Listbox(self.top, height=10)
        self.font_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.scrollbar = ttk.Scrollbar(
            self.top, orient=tk.VERTICAL, command=self.font_listbox.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.font_listbox.configure(yscrollcommand=self.scrollbar.set)
        # Populate the font list
        self.fonts_list = list(font.families())
        self.fonts_list.sort()
        for f in self.fonts_list:
            self.font_listbox.insert(tk.END, f)

        # Example Label
        self.example_label = tk.Label(self.top, text="Font Preview", font=self.font)
        self.example_label.pack(pady=5)

        self.example_label1 = tk.Label(
            self.top,
            text="A B  C D E F G H I J K L M N O P Q R S T U V W X Y Z",
            font=self.font,
        )
        self.example_label1.pack(pady=5)
        self.example_label3 = tk.Label(
            self.top,
            text="a b c d e f g h j k l m n o p q r s t u v w x y z",
            font=self.font,
        )
        self.example_label3.pack(pady=5)
        self.example_label4 = tk.Label(
            self.top, text="The brown fox jumps over the city", font=self.font
        )
        self.example_label4.pack(pady=5)
        # Font size selector
        tk.Label(self.top, text="Select Font Size:").pack()
        self.font_size_var = tk.IntVar(value=self.font.cget("size"))
        self.font_size_spinbox = ttk.Spinbox(
            self.top,
            from_=8,
            to=72,
            textvariable=self.font_size_var,
            width=5,
            command=self.update_font_example,
        )
        self.font_size_spinbox.pack(pady=5)

        # Buttons
        tk.Button(
            self.top, bd=5, bg="lightblue", text="Apply", command=self.apply_font
        ).pack(side=tk.LEFT, padx=5, pady=10)
        tk.Button(
            self.top, bd=3, bg="light pink", text="Close", command=self.top.destroy
        ).pack(side=tk.RIGHT, padx=5, pady=10)
        tk.Button(
            self.top, bd=6, bg="seashell3", text="Default", command=self.default
        ).pack(side=tk.LEFT, padx=5, pady=10)
        # Bind font selection
        self.font_listbox.bind("<<ListboxSelect>>", self.update_font_example)

    def update_font_example(self, event=None):
        # Update the font preview based on selection
        selected_font = (
            self.font_listbox.get(self.font_listbox.curselection())
            if self.font_listbox.curselection()
            else self.font.cget("family")
        )
        font_size = self.font_size_var.get()
        self.example_label.config(font=(selected_font, font_size))
        self.example_label1.config(font=(selected_font, font_size))
        self.example_label3.config(font=(selected_font, font_size))
        self.example_label4.config(font=(selected_font, font_size))

    def apply_font(self):
        # Apply the selected font and size to the text widget
        selected_font = (
            self.font_listbox.get(self.font_listbox.curselection())
            if self.font_listbox.curselection()
            else self.font.cget("family")
        )
        font_size = self.font_size_var.get()
        self.textwidget.config(font=(selected_font, font_size))
        self.textwidget.update_idletasks()

    def default(self):
        default_font = "Consolas"
        default_size = 12

        # Apply the default font and size to the text widget
        self.textwidget.config(font=(default_font, default_size))
        self.textwidget.update_idletasks()


######################CODE FORMATTER CLASS##########################################
class CodeFormatterApp:
    def __init__(self, root, textwidget):
        self.root = root
        self.textwidget = textwidget      
        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid expansion
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # Create tabs
        self._create_original_code_tab()
        self._create_formatted_code_tab()
        self._create_linter_output_tab()
        
        # Track the original file path
        self.original_file_path = None
    
    def _create_original_code_tab(self):
        """Create the Original Code tab."""
        tab_original = ttk.Frame(self.notebook)
        self.notebook.add(tab_original, text="Original Code")
        
        tab_original.rowconfigure(0, weight=1)
        tab_original.columnconfigure(0, weight=1)
        
        self.text_original = tk.Text(tab_original,bd=15,bg="azure", wrap="word")
        self.text_original.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.content = self.textwidget.get(1.0, tk.END)
        self.text_original.insert(1.0, self.content)
        btn_load = tk.Button(tab_original, text="Load Code", command=self.load_file)
        btn_load.grid(row=1, column=0, pady=5)

    def _create_formatted_code_tab(self):
        """Create the Formatted Code tab."""
        tab_formatted = ttk.Frame(self.notebook)
        self.notebook.add(tab_formatted, text="Formatted Code")
        
        tab_formatted.rowconfigure(0, weight=1)
        tab_formatted.columnconfigure(0, weight=1)
        
        self.text_formatted = tk.Text(tab_formatted, wrap="word", state="normal")
        self.text_formatted.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        btn_black = tk.Button(tab_formatted, text="Format with Black if Load Btn", command=self.format_with_black)
        btn_black.grid(row=1, column=0, padx=5, pady=5)
       
        btn_autopep8 = tk.Button(tab_formatted, text="Format with Autopep8", command=self.format_with_autopep8)
        btn_autopep8.grid(row=1, column=1, padx=5, pady=5)
        
        btn_save = tk.Button(tab_formatted, text="Save Code", command=self.save_formatted_code)
        btn_save.grid(row=2, column=0, columnspan=2, pady=5)
        btn_end = tk.Button(tab_formatted, text="Close Formatter", command=self.closeout)
        btn_end.grid(row=4, column=1)
        logging.basicConfig(level=logging.DEBUG, filename="formatter_debug.log", filemode="w")

    def _create_linter_output_tab(self):
        """Create the Linter Output tab."""
        tab_linter = ttk.Frame(self.notebook)
        self.notebook.add(tab_linter, text="Linter Output")
        
        tab_linter.rowconfigure(0, weight=1)
        tab_linter.columnconfigure(0, weight=1)
        
        self.text_linter = tk.Text(tab_linter, wrap="word", state="normal")
        self.text_linter.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        btn_lint = tk.Button(tab_linter, text="Run Linter", command=self.lint_with_pylint)
        btn_lint.grid(row=1, column=0, pady=5)

    def load_file(self):
        """Load a Python file into the Original Code tab."""
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.original_file_path = file_path
            with open(file_path, "r") as file:
                self.text_original.delete("1.0", tk.END)
                self.text_original.insert("1.0", file.read())

    def format_with_black(self, file_path):
        """Format a Python file using Black via subprocess."""
        try:
            result = subprocess.run(
                ["black", file_path],
                text=True,
                capture_output=True,
                check=False
            )
            if result.returncode == 0:
                return f"Black formatting applied successfully:\n{result.stdout}"
            return f"Black formatting failed:\n{result.stderr}"
        except FileNotFoundError:
            return "Black is not installed or not in the system PATH."
        except Exception as e:
            return f"Unexpected error running Black: {str(e)}"

    def format_with_autopep8(self):
        """Format code using Autopep8 and display it in the Formatted Code tab."""
        self._update_output(self.text_original, self.text_formatted, self._format_with_autopep8)

    def run_linter(self):
        """Run a linter on the code and display the output in the Linter Output tab."""
        self._update_output(self.text_original, self.text_linter, self._lint_code)

   
    
    def save_formatted_code(self):
        """Save the formatted code to a file with a unique name."""
        formatted_code = self.text_formatted.get("1.0", tk.END).strip()
        if not formatted_code:
            messagebox.showerror("Error", "No formatted code to save!")
            return
        
        # Determine save path
        if self.original_file_path:
            base_name = self.original_file_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        else:
            base_name = "formatted_code"
        unique_filename = f"{base_name}_{int(time.time())}.py"
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            initialfile=unique_filename,
            filetypes=[("Python Files", "*.py")]
        )
        
        if save_path:
            with open(save_path, "w") as file:
                file.write(formatted_code)
            messagebox.showinfo("Success", f"Formatted code saved to {save_path}!")

    def _update_output(self, input_text, output_text, processor):
        """Update the output tab with processed results."""
        original_code = input_text.get("1.0", tk.END).strip()
        if not original_code:
            messagebox.showerror("Error", "No code to process!")
            return
        try:
            result = processor(original_code)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))


   
    def _format_with_autopep8(self, code):
        """Format code using Autopep8."""
        return autopep8.fix_code(code)
    def lint_with_pylint(self):
        """Lint code using Pylint via subprocess without temporary files."""
        try:
            code = self.text_original.get("1.0", tk.END).strip()
            if not code:
                messagebox.showerror("Error", "No code to lint!")
                return
            
            result = subprocess.run(
                ["pylint", "--from-stdin", "dummy_file.py"],  # Pylint expects a filename for context
                input=code,
                text=True,
                capture_output=True
            )
            
            return result.stdout if result.returncode == 0 else result.stderr
        except FileNotFoundError:
            return "Pylint is not installed or not in PATH."
        except Exception as e:
            return f"Error running Pylint: {str(e)}"




    def format_with_black(self):
        """Format code using Black. Uses the current file if no path is provided."""
        if not self.original_file_path:
            messagebox.showerror("Error", "No file loaded to format with Black.")
            return
        try:
            result = subprocess.run(
                ["black", self.original_file_path],
                text=True,
                capture_output=True,
                check=False
            )
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Black formatting applied:\n{result.stdout}")
               
            else:
                messagebox.showerror("Error", f"Black formatting failed:\n{result.stderr}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Black is not installed or not in the PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error running Black: {str(e)}")

    def lint_with_pylint(self):
        """Run Pylint on the loaded file."""
        if not self.original_file_path:
            messagebox.showerror("Error", "No file loaded to lint with Pylint.")
            return
        try:
            result = subprocess.run(
                ["pylint", self.original_file_path],
                text=True,
                capture_output=True,
                check=False
            )
            if result.returncode in (0, 32):  # 32: warnings/errors
                self.text_linter.delete("1.0", tk.END)
                self.text_linter.insert("1.0", result.stdout)
            else:
                messagebox.showerror("Error", f"Pylint failed:\n{result.stderr}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Pylint is not installed or not in the PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error running Pylint: {str(e)}")
     
    def closeout(self):
        self.root.destroy()


    def _update_output(self, input_text, output_text, processor):
        """Update the output tab with processed results."""
        original_code = input_text.get("1.0", tk.END).strip()
        if not original_code:
            messagebox.showerror("Error", "No code to process!")
            return
        try:
            logging.debug(f"Processing code: {original_code[:100]}...")  # Log first 100 characters
            result = processor(original_code)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", result)
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
            
######################################END######################################


if __name__ == "__main__":
    root = tk.Tk()
    root.title = "PyCode Edit and Formatter"
    root.geometry("1000x700")
    pycode_tab_editor = MultiTabTextEditor(root)
    root.mainloop()
