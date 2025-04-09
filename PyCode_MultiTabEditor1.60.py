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
from datetime import datetime





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
        self.file_menu.add_command(label="Open File Browser", command=self.open_file_browser)

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menubar,background="PaleGreen1", tearoff=0)
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
        self.view_menu = tk.Menu(self.menubar, background="thistle", tearoff=0)
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
        self.menubar.add_cascade(label="Custom", menu=self.custom_menu)

        # About menu
        self.about_menu = tk.Menu(self.menubar, background="lavender",tearoff=0)
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

    def get_current_text_widget(self):
        current_tab = self.notebook.select()  # Get the currently selected tab
        current_widget = self.notebook.nametowidget(current_tab)
        self.textwidget = current_widget
        return self.textwidget  
    def add_tab(self):
        tab = tk.Frame(self.notebook)
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
            self.textwidget.delete(1.0, tk.END)  # Clear existing content
            self.textwidget.insert(1.0, content)  # Load file content
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
      
            self.textwidget.delete(1.0, tk.END)
            with open(self.file_name) as f:
                self.textwidget.insert(1.0, f.readlines())

    def save_incremented_version(self):
        if not self.file_name:
            full_path = os.path.abspath(__file__)
            directory_= os.path.dirname(full_path)
            filename = os.path.basename(full_path)
            self.file_name = filename       
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
        full_path = os.path.abspath(__file__)
        self.file_name = os.path.basename(full_path)

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
            output_text.insert(1.0, "=== Standard Output ===\n")
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
        self.textwidget.tag_add("sel", 1.0, "end")
        return "break"

    def clear_clipboard(self):
        pass
      

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
            full_text = self.textwidget.get(1.0, "end-1c")

            # Use a regular expression to remove lines starting with `#` (ignoring leading whitespace)
            uncommented_text = "\n".join(
                line
                for line in full_text.split("\n")
                if not line.strip().startswith("#")
            )

            # Replace the content of the text widget with the uncommented text
            self.textwidget.delete(1.0, "end")
            self.textwidget.insert(1.0, uncommented_text)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while removing comments: {str(e)}"
            )

    def remove_comments(self):
        try:
            # Get the entire text from the text widget
            full_text = self.textwidget.get(1.0, "end-1c")
            uncommented_text = "\n".join(
                line
                for line in full_text.split("\n")
                if not line.strip().startswith("#")
            )

            # Replace the content of the text widget with the uncommented text
            self.textwidget.delete(1.0, "end")
            self.textwidget.insert(1.0, uncommented_text)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while removing comments: {str(e)}"
            )

    def remove_text_between_quotes(self, quote_type="all"):
        try:
            # Get the full content of the text widget
            full_text = self.textwidget.get(1.0, "end-1c")

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
            self.textwidget.delete(1.0, "end")
            self.textwidget.insert(1.0, updated_text)
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
        content = current_textwidget.get(1.0, "end-1c")

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
            full_text = self.textwidget.get(1.0, "end-1c")

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
            self.textwidget.delete(1.0, "end")
            self.textwidget.insert(1.0, new_content)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while moving imports: {str(e)}"
            )

    def remove_text_between_quotes(self, quote_type="all"):
        try:
            # Get the full content of the text widget
            full_text = self.textwidget.get(1.0, "end-1c")

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
            self.textwidget.delete(1.0, "end")
            self.textwidget.insert(1.0, updated_text)
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
        full_text = self.textwidget.get(1.0, "end-1c")
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
        self.textwidget.delete(1.0, "end")
        self.textwidget.insert(1.0, new_text)

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
            full_text = self.textwidget.get(1.0, "end-1c")

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
            self.textwidget.delete(1.0, "end")
            self.textwidget.insert(1.0, new_content)
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while moving imports: {str(e)}"
            )

  

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

    def open_file_browser(self):
        self.top = Toplevel()
        self.top.wm_attributes("-topmost", True)  # Make the window always on to
        self.frm = tk.Frame(self.top)
        self.frm.grid(row=0, column=0)
        self.path = os.getcwd()
        self.file_extensions = [".txt", ".py", ".md", ".html"]
        self.dirpath = tk.Entry(self.frm, bd=12, bg="seashell")
        self.dirpath.grid(row=0, column=0, sticky="ew")
        self.dirpath.insert(tk.END, self.path)
        self.scrollbar = tk.Scrollbar(self.frm,bd=5,bg="cyan", orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.lb = tk.Listbox(self.frm, bg="seashell", height=20, width=60, exportselection=True, yscrollcommand=self.scrollbar.set)
        self.lb.grid(row=1, column=0, sticky="nsew")
        self.lb.bind("<<ListboxSelect>>", self.on_file_select)
        self.list_files(self.path)
        self.scrollbar.config(command=self.lb.yview)
        self.btn = tk.Button(self.frm, text="Change Directory", bd=5, bg="azure", command=self.newdirlist)
        self.btn.grid(row=2, column=0, sticky="ew")
        self.recursive_btn = tk.Button(self.frm, text="Recursive Directories", bd=5, bg="cornsilk", command=self.recursive_new_list)
        self.recursive_btn.grid(row=3, column=0, sticky="ew")

    def on_file_select(self, event):
        selection = self.lb.curselection()
        if selection:
            filename = self.lb.get(selection[0])
            self.display_text(filename)

    def list_files(self, directory):
        self.lb.delete(0, tk.END)
        for file in os.listdir(directory):
            if any(file.endswith(ext) for ext in self.file_extensions):
                self.lb.insert(tk.END, file)
    
    def newdirlist(self):
        self.path = filedialog.askdirectory()
        if self.path:
            self.dirpath.delete(0, tk.END)
            self.dirpath.insert(tk.END, self.path)
            self.list_files(self.path)

    def recursive_new_list(self):
        self.path = filedialog.askdirectory()
        if self.path:
            self.dirpath.delete(0, tk.END)
            self.dirpath.insert(tk.END, self.path)
            self.lb.delete(0, tk.END)
            threading.Thread(target=self._load_files_generator, daemon=True).start()

    def _file_generator(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    yield os.path.join(root, file)

    def _load_files_generator(self):
        for file in self._file_generator(self.path):
            self.lb.after(0, self.lb.insert, tk.END, file)
  
    def _search_files(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    self.lb.after(0, self.lb.insert, tk.END, os.path.join(root, file))
                   
   

    def adjust_entry_width(self):
        path_length = len(self.path)
        new_width = max(60, path_length + 5)
        self.dirpath.config(width=new_width)

    def display_text(self, filename, event=None):
        try:
            #self.textwidget = self.get_current_text_widget()
            if not self.textwidget:
                raise ValueError("No active text widget found.")
            with open(filename, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                self.textwidget.delete(1.0, tk.END)
                self.textwidget.insert(1.0, content)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def help(self):
        help1 = """
        don't read doc"""
        messagebox.showinfo("Help", help1)
   

    def about(self):
        about_str = """
        This is a Custom Pycode Editor Application
            John Hewitt rev1 Jan 2025"""
        messagebox.showinfo("About", about_str)



class FindReplace:
    def __init__(self, textwidget):
        self.textwidget = textwidget
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
        self.textwidget.tag_remove("found", self.textwidget, tk.END)
        search_query = self.find_var.get()
        if search_query:
            content = self.textwidget.get(1.0, tk.END)
            idx = 1.0
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
        self.textwidget.tag_remove("found", 1.0, tk.END)
        content = self.textwidget.get(1.0, tk.END)
        if self.use_regex.get():
            try:
                replaced_content, count = re.subn(find_text, replace_text, content)
                if count > 0:
                    self.textwidget.delete(1.0, tk.END)
                    self.textwidget.insert(1.0, replaced_content)
            except re.error as e:
                messagebox.showerror("Regex Error", str(e))
        else:
            if find_text in content:
                replaced_content = content.replace(find_text, replace_text)
                self.textwidget.delete(1.0, tk.END)
                self.textwidget.insert(1.0, replaced_content)

    def replace_all_text(self):
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        if not find_text or not replace_text:
            return
        self.textwidget.tag_remove("found", 1.0, tk.END)
        try:
            if self.use_regex.get():
                content = self.textwidget.get(1.0, tk.END)
                replaced_content, _ = re.subn(find_text, replace_text)
                self.textwidget.delete(1.0, tk.END)
                self.textwidget.insert(1.0, replaced_content)
            else:
                content = self.textwidget.get(1.0, tk.END)
                replaced_content = content.replace(find_text, replace_text)
                self.textwidget.delete(1.0, tk.END)
                self.textwidget.insert(1.0, replaced_content)
        except re.error as e:
            messagebox.showerror("Regex Error", str(e))
####|(\"\"\"[\s\S]*?\"\"\"|\"\"\"[\s\S]*?\"\"\")"
##################################################################################
class SyntaxHighlite:
    def __init__(self, textwidget):
        self.textwidget = textwidget
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
        self.textwidget.tag_config("selfs", foreground="MediumOrchid4")
        self.textwidget.tag_config("classes", foreground="DeepSkyBlue3")
        self.textwidget.tag_config("docstring", background="light yellow",foreground="SpringGreen2")
        self.textwidget.tag_config("docstring2", foreground="SpringGreen2")

    def highlight_syntax(self, event=None):
        for tag in list(self.syntax_elements.keys()):
            self.textwidget.tag_remove(tag, 1.0, tk.END)

        for tag, pattern in list(self.syntax_elements.items()):
            start_index = 1.0
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
        self.textwidget.tag_remove("match", 1.0, tk.END)

        matches_found = 0
        if needle:
            start_pos = 1.0
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



######################################END######################################


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    pycode_tab_editor = MultiTabTextEditor(root)
    root.mainloop()
