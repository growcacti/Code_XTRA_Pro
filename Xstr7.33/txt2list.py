import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

class TextToListConverter:
    def __init__(self, parent):
        self.parent = parent
       
        self.last_directory = os.getcwd()  # Initialize last_directory
        self.setup_widgets()

    def setup_widgets(self):
        self.txtwidget = tk.Text(self.parent, height=10, width=50)
        self.txtwidget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        convert_button_lines = tk.Button(self.parent, text="Lines to list", command=self.text_to_line_list)
        convert_button_lines.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        clear_list_button = tk.Button(self.parent, text="Clear Lists", command=self.clear_list)
        clear_list_button.grid(row=2, column=0)

        self.listbox_lines = tk.Listbox(self.parent, width=25, height=10)
        self.listbox_lines.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.listbox_words = tk.Listbox(self.parent, width=25, height=10)
        self.listbox_words.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        save_button_lines = tk.Button(self.parent, text="Save Line List", command=self.save_line_list)
        save_button_lines.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        convert_button_words = tk.Button(self.parent, text="Convert Text to Word List", command=self.text_to_word_list)
        convert_button_words.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        add_quotes_button = tk.Button(self.parent, text="Add Quotes", command=self.add_quotes_to_word_list)
        add_quotes_button.grid(row=2, column=2)

        load_text_button = tk.Button(self.parent, text="Load Text", command=self.load_text_file)
        load_text_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        save_button_words = tk.Button(self.parent, text="Save Word List", command=self.save_word_list)
        save_button_words.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        for i in range(4):
            self.parent.grid_columnconfigure(i, weight=1)

    def clear_list(self):
        """Clears all items from the listboxes."""
        self.listbox_lines.delete(0, tk.END)
        self.listbox_words.delete(0, tk.END)

    def text_to_word_list(self):
        """Converts text in the text widget to a list of words and displays it in the listbox."""
        self.listbox_words.delete(0, tk.END)
        words = set(self.txtwidget.get("1.0", tk.END).strip().split())
        for word in sorted(words):
            self.listbox_words.insert(tk.END, word)

    def text_to_line_list(self):
        """Converts text in the text widget to a list of lines and displays it in the listbox."""
        self.listbox_lines.delete(0, tk.END)
        text_contents = self.txtwidget.get("1.0", tk.END).strip().split('\n')
        for item in text_contents:
            self.listbox_lines.insert(tk.END, item)

    def add_quotes_to_word_list(self):
        """Adds quotes to each word in the word list."""
        words_with_quotes = [f'"{self.listbox_words.get(idx)}"' for idx in range(self.listbox_words.size())]
        self.listbox_words.delete(0, tk.END)
        for word in words_with_quotes:
            self.listbox_words.insert(tk.END, word)

    def load_text_file(self):
        """Loads text from a file into the text widget."""
        file_path = filedialog.askopenfilename(initialdir=self.last_directory, title="Select text file", filetypes=(("Text files", "*.txt"),("Python files", "*.py"),("All files", "*.*")))
        if file_path:
            try:
                with open(file_path, "r") as file:
                    text_content = file.read()
                self.txtwidget.delete("1.0", tk.END)  # Clear existing text
                self.txtwidget.insert("1.0", text_content)  # Insert new text
                self.last_directory = os.path.dirname(file_path)  # Update last directory
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load text: {e}")

    def save_line_list(self):
        """Saves the lines list to a file."""
        lines = [self.listbox_lines.get(idx) for idx in range(self.listbox_lines.size())]
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            with open(filepath, 'w') as file:
                for line in lines:
                    file.write(line + '\n')

    def save_word_list(self):
        """Saves the words list to a file."""
        words = [self.listbox_words.get(idx) for idx in range(self.listbox_words.size())]
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            with open(filepath, 'w') as file:
                for word in words:
                    file.write(word + '\n')

##if __name__ == "__main__":
##    parent = tk.Tk()
##    app = TextToListConverter(parent)
##    parent.mainloop()
##
