
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory




class CodeEditorApp:
    def __init__(self, root):
        self.parent = root
        self.create_widgets()

    def create_widgets(self):
        self.entry = tk.Entry(self.parent)
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.lbox = tk.Listbox(self.parent,  selectmode='multiple')
        self.lbox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.button1 = tk.Button(self.parent, text="Insert Code",command=self.insert_code)
        self.button1.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.button2 = tk.Button(self.parent, text="Insert Word ",command=self.insert_word)
        self.button2.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.button3 = tk.Button(self.parent, text="Load List",command=self.populate_lbox)
        self.button3.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.button4 = tk.Button(self.parent, text="Clear Selection",command=self.clear_selection)
        self.button4.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.button5 = tk.Button(self.parent, text="Clear Textbox",command=self.cleartext)
        self.button5.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.button6 = tk.Button(self.parent, text="Clear Lbox",command=self.clearlbox)
        self.button6.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.button7 = tk.Button(self.parent, text="future senout",command=self.sendtextout)
        self.button7.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        self.textwidget = ScrolledText(self.parent, height=10)
        self.textwidget.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        

    def insert_code(self):
        selected_indices = self.lbox.curselection()
        for index in selected_indices:
            selected_line = self.lbox.get(index)
            self.textwidget.insert(tk.END, f"{selected_line}\n")

    def populate_lbox(self):
        file_path = askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.lbox.delete(0, tk.END)
                for line in file:
                    self.lbox.insert(tk.END, line.strip())  


    def insert_word(self):
        try:
            self.word = self.entry.get()
            start_index = self.textwidget.index("sel.first")
            end_index = self.textwidget.index("sel.last")

            selected_text = self.textwidget.get(start_index, end_index)
            new_lines = [
                self.word + line.strip() if line.strip() else line
                for line in selected_text.split("\n")
            ]
            new_text = "\n".join(new_lines)

            self.textwidget.delete(start_index, end_index)
            self.textwidget.insert(start_index, new_text)
        except tk.TclError:
            mb.showinfo("No Selection", "Please select some text to insert the word.")

    def clear_selection(self, event=None):
        self.lbox.tag_remove(tk.SEL, "1.0", tk.END)



    def cleartext(self):
        self.textwidget.delete("1.0", tk.END)


    def clearlbox(self):
        self.lbox.delete(0, tk.END)


    def sendtextout(self):
        self.output = self.textwidget.get("1.0", tk.END)
        self.text2.insert(tk.END, self.output)


        
            
