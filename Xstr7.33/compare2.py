import tkinter as tk
from tkinter import ttk, INSERT,END,font,Toplevel
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText


from txinfo2 import *

class TextFileComparator:
    def __init__(self, parent):
        self.parent = parent
        self.text1 = None
        self.text2 = None
        self.output_text = None
        self.btfr = ttk.Frame(parent, width=10, height=10)
        self.btfr.grid(row=0, column=0)
        self.txtfrm1 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm1.grid(row=0, column=1)
        self.txtfrm2 = ttk.Frame(self.parent, width=60, height=60)
        self.txtfrm2.grid(row=0, column=2)
        self.txtfrm3 = ttk.Frame(self.parent, width=50, height=15)
        self.txtfrm3.grid(row=12, column=0, columnspan=4)
        
    def create_gui(self):
        # Create text widgets for displaying the files
        self.text1 = ScrolledText(self.txtfrm1)
        self.text1.grid(row=0, column=0, sticky="nsew")

        self.text2 = ScrolledText(self.txtfrm2)
        self.text2.grid(row=0, column=0, sticky="nsew")

        # Create the output text widget
        self.output_text = tk.Text(self.txtfrm3, height=15)
        self.output_text.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Create a button to load the files
        load_button = tk.Button(self.btfr, text="Load Files", command=self.load_files)
        load_button.grid(row=2, column=0, sticky="w")

        # Create a button to compare the files
        compare_button = tk.Button(
            self.btfr, text="Compare", command=self.compare_files
        )
        compare_button.grid(row=3, column=0, sticky="w")

        # Create a button to clear all text widgets
        clear_button = tk.Button(
            self.btfr, text="Clear All", command=self.clear_textwidgets
        )
        clear_button.grid(row=4, column=0, sticky="w")
        self.infotxt1 =  TextWidgetInfo(self.txtfrm1, self.text1)
        self.infotxt2 =  TextWidgetInfo(self.txtfrm2, self.text2)
        self.outtxtinfo =TextWidgetInfo(self.txtfrm3, self.output_text)
    def clear_textwidgets(self):
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

    def load_files(self):
        file1 = filedialog.askopenfilename(title="Select First File")
        if file1:
            with open(file1, "r") as f:
                content = f.read()
                self.text1.delete("1.0", tk.END)
                self.text1.insert(tk.END, content)

        file2 = filedialog.askopenfilename(title="Select Second File")
        if file2:
            with open(file2, "r") as f:
                content = f.read()
                self.text2.delete("1.0", tk.END)
                self.text2.insert(tk.END, content)

    def compare_files(self):
        # Get the content from the text widgets
        content1 = self.text1.get("1.0", tk.END)
        content2 = self.text2.get("1.0", tk.END)

        # Split the content into lines
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()

        # Initialize a counter for differences
        diff_count = 0

        # Clear the text widgets
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)

        # Compare the lines and highlight the differences
        diff_line_numbers = []
        for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
            if line1 != line2:
                # Increase the difference count
                diff_count += 1
                diff_line_numbers.append(i)

                # Highlight the difference by inserting tags
                self.text1.insert(tk.END, line1 + "\n", "diff")
                self.text2.insert(tk.END, line2 + "\n", "diff")
            else:
                # Insert the lines without any difference
                self.text1.insert(tk.END, line1 + "\n")
                self.text2.insert(tk.END, line2 + "\n")

        # Add the remaining lines, if any
        if len(lines1) > len(lines2):
            for line in lines1[len(lines2) :]:
                self.text1.insert(tk.END, line + "\n")
                diff_count += 1
                diff_line_numbers.append(len(lines2) + 1)
        elif len(lines2) > len(lines1):
            for line in lines2[len(lines1) :]:
                self.text2.insert(tk.END, line + "\n")
                diff_count += 1
                diff_line_numbers.append(len(lines1) + 1)

        # Configure the tag for highlighting differences
        self.text1.tag_configure("diff", background="wheat1")
        self.text2.tag_configure("diff", background="sky blue")

        # Show the difference count and line numbers
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Number of differences: {diff_count}\n")
        self.output_text.insert(tk.END, f"Lines in Text 1: {len(lines1)}\n")
        self.output_text.insert(tk.END, f"Lines in Text 2: {len(lines2)}\n")
        self.output_text.insert(tk.END, "Line numbers with differences: ")
        self.output_text.insert(tk.END, ", ".join(map(str, diff_line_numbers)))

    def update_info(self, event=None):
        self.content = self.text1.get("1.0", "end-1c")
        self.content2 = self.text2.get("1.0", "end-1c")

      
        
        
        self.content = self.textwidget.get("1.0", "end-1c")

        # Count the lines, words, and characters
        self.infotxt1.update()
        self.infotxt2.update()
        self.outtxtinfo.update()
             

    def run(self):
        self.create_gui()
