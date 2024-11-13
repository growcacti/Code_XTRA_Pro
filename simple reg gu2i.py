import tkinter as tk
from tkinter import messagebox
import re


root = tk.Tk()
root.title("Regex Text Processor")


entry_text = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_text)
entry.pack()


def process_text():
    input_text = entry_text.get()
    # Example regex operation: find all email addresses
    pattern = r"[a-zA-Z0-9._%+-]+="
    matches = re.findall(pattern, input_text)
    messagebox.showinfo("Matches", "\n".join(matches))


process_btn = tk.Button(root, text="Process Text", command=process_text)
process_btn.pack()



textwidget=tk.Text(root)
textwidget.pack()
root.mainloop()
