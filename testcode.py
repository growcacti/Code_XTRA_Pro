import tkinter as tk
from tkinter import messagebox
import re

root = tk.Tk()
root.title("Regex Text Processor")

textwidget = tk.Text(root)
textwidget.pack()

def process_text():
    content = textwidget.get("1.0", tk.END)
    lines = content.splitlines()
    modified_content = ""
    
    char = '#'  # Character to remove up to
    pattern = rf"^(.*?){re.escape(char)}"  # Match everything up to and including the character
    
    for line in lines:
        new_line = re.sub(pattern, '', line, 1)  # Replace the matched content with empty string
        modified_content += f"{new_line}\n"
    
    textwidget.delete("1.0", tk.END)  # Clear the text widget
    textwidget.insert("1.0", modified_content.rstrip("\n"))  # Insert modified content, remove trailing newline

process_btn = tk.Button(root, text="Process Text", command=process_text)
process_btn.pack()

root.mainloop()
