import tkinter as tk
from tkinter import Toplevel, END, messagebox
import re

class Find_Replace:
    def __init__(self, root, textwidget):
        self.root = root
        self.textwidget = textwidget
        self.textwidget.grid(row=0, column=0, sticky="nsew")
          
        self.find_str = tk.StringVar()
        self.find_str.trace('w', self.on_find_text_change)  # Trace changes
        
        self.replace_str = tk.StringVar()
        self.use_regex = tk.BooleanVar()  # Variable to track regex mode
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.create_find_replace_interface()

    def create_find_replace_interface(self):
        self.top = Toplevel()
        self.top.title("Find & Replace")
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()

      

        # Set up trace on the variables
        self.find_var.trace("w", lambda name, index, mode, sv=self.find_var: self.on_entry_change())
        self.replace_var.trace("w", lambda name, index, mode, sv=self.replace_var: self.on_entry_change())

        tk.Label(self.top, text="Find:").grid(row=0, column=0, padx=4, pady=4)
        self.find_entry = tk.Entry(self.top, width=20, background="cornsilk")
        self.find_entry.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(self.top, text="Replace With:").grid(row=1, column=0, padx=4, pady=4)
        self.replace_entry = tk.Entry(self.top, width=20, background="seashell")
        self.replace_entry.grid(row=1, column=1, padx=4, pady=4)

        # Checkbox for toggling regex mode
        tk.Checkbutton(self.top, text="Use Regex", variable=self.use_regex).grid(row=2, column=0, columnspan=2)

        find_btn = tk.Button(self.top, text="Find Next", command=lambda: self.find_text(self.find_entry.get()))
        find_btn.grid(row=3, column=0, padx=4, pady=4)
       
        replace_btn = tk.Button(self.top, text="Replace", command=lambda: self.replace_text(self.find_entry.get(), self.replace_entry.get()))
        replace_btn.grid(row=3, column=1, padx=4, pady=4)

        replace_all_btn = tk.Button(self.top, text="Replace All", command=lambda: self.replace_all_text(self.find_entry.get(), self.replace_entry.get()))
        replace_all_btn.grid(row=4, column=1, padx=4, pady=4)

        regex_help_btn = tk.Button(self.top, text="Regex Help", command=self.regex_help)
        regex_help_btn.grid(row=5, column=0, columnspan=2, pady=4)

        self.find_entry.focus_set()
        self.find_entry.bind("<Return>", lambda event: self.find_text(self.find_var.get()))
        self.replace_entry.bind("<Return>", lambda event: self.replace_text(self.find_var.get(), self.replace_var.get()))

    def regex_help(self):
        # Help text for regex
        help_text = """
        Common Regex Patterns:
        - ^abc: Matches any string that starts with 'abc'
        - abc$: Matches any string that ends with 'abc'
        - [a-zA-Z]: Matches any single letter
        - \\d: Matches any digit
        - .*: Matches any character (except for newline characters)
        - ab|cd: Matches 'ab' or 'cd'
        """
        messagebox.showinfo("Regex Help", help_text)



    def find_text(self, search_query):
        self.textwidget.tag_remove("found", "1.0", END)
        if search_query:
            content = self.textwidget.get("1.0", END)
            idx = "1.0"
            last_idx = None
            lastidx = None  # Initialize lastidx to ensure it's always defined
            try:
                if self.use_regex.get():
                    for match in re.finditer(search_query, content):
                        start, end = match.start(), match.end()
                        start_idx = self.textwidget.index(f"{idx}+{start}c")
                        end_idx = self.textwidget.index(f"{idx}+{end}c")
                        self.textwidget.tag_add("found", start_idx, end_idx)
                        last_idx = start_idx
                        lastidx = end_idx  # Update lastidx here for regex matches
                else:
                    while True:
                        idx = self.textwidget.search(search_query, idx, nocase=1, stopindex=END)
                        if not idx:
                            break
                        last_idx = idx
                        lastidx = f"{idx}+{len(search_query)}c"
                        self.textwidget.tag_add("found", idx, lastidx)
                        idx = f"{lastidx}+1c"
                
                if last_idx:  # Check if last_idx was set, indicating at least one match was found
                    self.textwidget.tag_config("found", background="purple", foreground="yellow")
                    self.textwidget.see(last_idx)
                    self.textwidget.mark_set("insert", last_idx)
                    self.textwidget.focus()
            except re.error as e:
                messagebox.showerror("Regex Error", str(e))







        
    def replace_all_text(self, find_text, replace_text):
        if not find_text or not replace_text:
            return
        self.textwidget.tag_remove("found", "1.0", END)
        if self.use_regex.get():
            try:
                content = self.textwidget.get("1.0", END)
                replaced_content, _ = re.subn(find_text, replace_text, content)
                self.textwidget.delete("1.0", END)
                self.textwidget.insert("1.0", replaced_content)
            except re.error as e:
                messagebox.showerror("Regex Error", str(e))
        else:
            # Here's the implementation for non-regex replace all functionality
            content = self.textwidget.get("1.0", END)
            replaced_content = content.replace(find_text, replace_text)
            self.textwidget.delete("1.0", END)
            self.textwidget.insert("1.0", replaced_content)
    def replace_text(self, find_text, replace_text):
        if not find_text or not replace_text:
            return
        self.textwidget.tag_remove("found", "1.0", END)
        content = self.textwidget.get("1.0", END)
        
        # Check if regex mode is enabled
        if self.use_regex.get():
            try:
                # Using regex to find and replace
                replaced_content, count = re.subn(find_text, replace_text, content)
                if count > 0:  # If any replacements were made, update the widget's content
                    self.textwidget.delete("1.0", END)
                    self.textwidget.insert("1.0", replaced_content)
            except re.error as e:
                messagebox.showerror("Regex Error", str(e))
        else:
            # Non-regex find and replace
            if find_text in content:  # Check if the find_text exists in the content
                replaced_content = content.replace(find_text, replace_text)
                self.textwidget.delete("1.0", END)
                self.textwidget.insert("1.0", replaced_content)

   

    def replace_text(self, find_text, replace_text):
        if not find_text or not replace_text:
            return
        self.textwidget.tag_remove("found", "1.0", END)
        start_index = "1.0"
        while True:
            if self.use_regex.get():
                match = re.search(find_text, self.textwidget.get(start_index, END))
                if not match:
                    break
                start_index = self.textwidget.index(f"{start_index}+{match.start()}c")
                end_index = self.textwidget.index(f"{start_index}+{match.end()-match.start()}c")
            else:
                start_index = self.textwidget.search(find_text, start_index, stopindex=END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(find_text)}c"

            self.textwidget.delete(start_index, end_index)
            self.textwidget.insert(start_index, replace_text)
            start_index = f"{start_index}+{len(replace_text)}c"

    def replace_all_text(self, find_text, replace_text):
        if not find_text or not replace_text:
            return
        self.textwidget.tag_remove("found", "1.0", END)
        try:
            if self.use_regex.get():
                content = self.textwidget.get("1.0", END)
                replaced_content, _ = re.subn(find_text, replace_text, content)
                self.textwidget.delete("1.0", END)
                self.textwidget.insert("1.0", replaced_content)
            else:
                content = self.textwidget.get("1.0", END)
                replaced_content = content.replace(find_text, replace_text)
                self.textwidget.delete("1.0", END)
                self.textwidget.insert("1.0", replaced_content)
        except re.error as e:
            messagebox.showerror("Regex Error", str(e))

    def on_entry_change(self):
        # Cancel any existing after call
        if hasattr(self, 'after_id'):
            self.top.after_cancel(self.after_id)

        # Schedule a new after call
        self.after_id = self.top.after(500, self.perform_search)  # Delay in milliseconds

    def perform_search(self):
        search_query = self.find_var.get()
        # Implement search functionality here, which gets triggered after a delay
        # This could call find_text, replace_text, or similar functions based on the application's state
      
    def on_find_text_change(self, *args):
        # This method is called every time the find entry text changes.
        # Example use: Enable/disable the Replace All button based on input.
        find_text = self.find_str.get()
        if find_text:
            self.replace_button.config(state=tk.NORMAL)
        else:
            self.replace_button.config(state=tk.DISABLED)
    
    def start_replace_all(self):
        # Non-blocking replace all
        self.master.after(0, self.replace_all, self.find_str.get(), self.replace_str.get(), "1.0")

    def replace_all(self, find_text, replace_text, start):
        if not find_text:
            return  # Stop if find_text is empty
        
        idx = self.text_widget.search(find_text, start, nocase=1, stopindex='end')
        if not idx:
            messagebox.showinfo("Complete", "Replacement Complete")
            return  # Stop if no more occurrences
        
        lastidx = f"{idx}+{len(find_text)}c"
        self.text_widget.delete(idx, lastidx)
        self.text_widget.insert(idx, replace_text)

        # Schedule the next replacement
        self.master.after(1, self.replace_all, find_text, replace_text, lastidx)

