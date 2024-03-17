import tkinter as tk
from tkinter import ttk, font
import tkinter as tk
from tkinter import ttk, INSERT,END,font,Toplevel
from tkinter import messagebox as mb

from tkinter.font import Font, families
import os




class FontBar():
    def __init__(self, parent,textwidget):
        
        self.path = os.getcwd()
        self.textwidget = textwidget
        self.parent = parent
        self.fram = tk.Frame(self.parent)
        self.fram.grid(row=0, column=0, sticky="w")  # Align with the frame
       
        self.fram2 = ttk.Frame(self.parent)
        self.fram2.grid(row=3,column=0)
        self.toolbarfrm = tk.Frame(self.fram, width=10, height=100)
        self.toolbarfrm.grid(row=0, column=0, columnspan=5, sticky="w")
        self.shortcutbar = tk.Frame(self.fram2, height=10, width=80)
        self.shortcutbar.grid(row=0, column=1, columnspan=5, sticky="ew")
        self.font_config()
        sorted_fonts = sorted(families())  # Sort the list of font families
       
              

    def font_config(self):
        self.toolbar = tk.Canvas(self.toolbarfrm, bg="seashell")
        self.toolbar.grid(row=0, column=0, columnspan=5, sticky="ew")
        self.toolbar.config(width=300, height=60)
        self.values = [n for n in range(2, 120, 2)]

        self.font_family = tk.StringVar(
            self.toolbar
        )  # string variable for storing value of font options from user
        self.fontbox = ttk.Combobox(
            self.toolbar, width=50, textvariable=self.font_family, state="readonly"
        )  # combobox
        self.fontbox["values"] = values=families()
        self.fontbox.set("Liberation Serif")
        self.fontbox.grid(row=0, column=0)
        # font box ends here

        # font size box
        self.size = tk.IntVar(self.toolbar)
        self.fontsize = ttk.Combobox(
            self.toolbar, width=20, values=self.values, textvariable=self.size
        )

        self.size.set(12)
        self.fontsize.grid(row=0, column=1)

        self.current_font_family = self.font_family
        self.current_font_size = self.size
        self.textwidget.configure(font=("Liberation Serif", 12))
        self.fontbox.bind("<<ComboboxSelected>>", lambda event: self.change_font)
        self.fontsize.bind("<<ComboboxSelected>>", lambda event: self.change_font_size)
        self.fontbox.bind("<ButtonRelease-1>", lambda event: self.change_font)

        self.font_btn = tk.Button(
            self.toolbar,
            text=" Set Font",
            bd=3,
            bg="blue violet",
            command=lambda: self.change_fonttype(
                self.fontbox.get(), self.fontsize.get()
            ),
        )
        self.font_btn.grid(row=1, column=0)
        self.font_btn2 = tk.Button(
            self.toolbar,
            text="set size Font",
            bd=3,
            bg="blue violet",
            command=lambda: self.change_font_size(self.fontsize.get()),
        )
        self.font_btn2.grid(row=1, column=1)
        self.color_btn = tk.Button(
            self.toolbar,
            text="Font color",
            bd=2,
            bg="goldenrod",
            command=lambda: self.change_font_color(),
        )
        self.color_btn.grid(row=1, column=2)
        self.bold_btn = tk.Button(
            self.toolbar, text="B", bd=3, bg="violet red", command=self.change_bold
        )
        self.bold_btn.grid(row=1, column=3)
        self.bold_btn2 = tk.Button(
            self.toolbar,
            text="All B",
            bd=2,
            bg="violet red",
            command=self.changeall_bold,
        )
        self.bold_btn2.grid(row=0, column=3)
        self.italic_btn = tk.Button(
            self.toolbar, text="i", bd=3, bg="lawn green", command=self.change_italic
        )
        self.italic_btn.grid(row=1, column=4)
        self.italic_btn2 = tk.Button(
            self.toolbar,
            text="All i",
            bd=3,
            bg="lawn green",
            command=self.changeall_italic,
        )
        self.italic_btn2.grid(row=0, column=4)
        self.underline_btn = tk.Button(
            self.toolbar, text="_", bd=3, bg="yellow", command=self.underline_text
        )
        self.underline_btn.grid(row=1, column=5)
        self.underline_btn2 = tk.Button(
            self.toolbar,
            text="All _",command=self.changeall_underline,
        )
        self.underline_btn2.grid(row=0, column=5)
        self.align_left_btn = tk.Button(
            self.toolbar, text="LT",command=self.align_left
        )
        self.align_left_btn.grid(row=1, column=6)
        self.align_center_btn = tk.Button(
            self.toolbar, text="CT", bd=3, bg="cyan", command=self.align_center
        )
        self.align_center_btn.grid(row=1, column=7)
        self.align_right_btn = tk.Button(
            self.toolbar, text="RT", bd=3, bg="light pink", command=self.align_right
        )
        self.align_right_btn.grid(row=1, column=8)
        self.clear_btn = tk.Button(
            self.toolbar, text="clear", bd=3, bg="light pink", command=self.clear
        )
        self.clear_btn.grid(row=0, column=8)
        # function to change font family
 
    def change_font(self, event=None):
        self.current_font_family = font_family.get()
        self.textwidget.configure(font=(self.current_font_family, self.current_font_size))
        self.fontsize.bind(
            "<<ComboboxSelected>>", lambda event: self.change_font_size()
        )
        self.fontbox.bind("<<ComboboxSelected>>", lambda event,: self.change_font())

    def change_fonttype(self, type, size):
        self.type = self.fontbox.get()
        self.size = self.fontsize.get()
        self.textwidget.configure(font=(self.type, self.size))

    # change font size
    def change_font_size(self, size, event=None):
        self.fontbox.bind("<<ComboboxSelected>>", lambda event: self.change_font_size)
        self.size = size
        self.current_font_size = self.fontsize.get()
        self.textwidget.configure(font=(self.fontbox.get(), self.size))
        self.fontbox.bind("<<ComboboxSelected>>", lambda event: self.change_font_size)

    def change_bold(self, event=None):
        """toggle only selected text"""
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

    # change to italic
    def change_italic(self, event=None):
        """making italic the selected text"""
        try:
            self.current_tags = self.textwidget.tag_names("sel.first")
            if "italic" in self.current_tags:
                self.textwidget.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.textwidget.tag_add("italic", "sel.first", "sel.last")
                italic_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
                italic_font.configure(slant="italic")
                self.textwidget.tag_configure("italic", font=italic_font)
        except tk.TclError:
            pass

    def underline_text(self, event=None):
        try:
            self.current_tags = self.textwidget.tag_names("sel.first")
            if "underline" in self.current_tags:
                self.textwidget.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.textwidget.tag_add("underline", "sel.first", "sel.last")
                underline_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
                underline_font.configure(underline=1)
                self.textwidget.tag_configure("underline", font=underline_font)
        except tk.TclError:
            pass

    # change font color
    def change_font_color(self, event=None):
        try:
            (rgb, hx) = tk.colorchooser.askcolor()
            self.textwidget.tag_add("color", "sel.first", "sel.last")
            self.textwidget.tag_configure("color", foreground=hx)
            # self.textwidget.tag_configure(rgb, foreground=hx)
        except tk.TclError as ex:
            print(ex)

    # left alignment
    def align_left(self, event=None):
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("left", justify=tk.LEFT)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "left")

    # center alignment
    def align_center(self, event=None):
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("center", justify=tk.CENTER)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "center")

    # text alignment right
    def align_right(self, event=None):
        text_content = self.textwidget.get(1.0, "end")
        self.textwidget.tag_config("right", justify=tk.RIGHT)
        self.textwidget.delete(1.0, tk.END)
        self.textwidget.insert(tk.INSERT, text_content, "right")

    def changeall_bold(self):
        self.textwidget.tag_add("bold", "1.0", "end")
        bold_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
        bold_font.configure(weight="bold")
        self.textwidget.tag_configure("bold", font=bold_font)

    def changeall_italic(self):
        self.textwidget.tag_add("italic", "1.0", "end")
        italic_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
        italic_font.configure(slant="italic")
        self.textwidget.tag_configure("italic", font=italic_font)

    def changeall_underline(self):
        self.textwidget.tag_add("underline", "1.0", "end")
        underline_font = tk.font.Font(self.textwidget, self.textwidget.cget("font"))
        underline_font.configure(underline=1)
        self.textwidget.tag_configure("underline", font=underline_font)

    def destory(self):
        self.fram.grid_forget()

    def clear(self):
        self.textwidget.delete("1.0", tk.END)
        

    def font_config(self):
        # Apply font configurations to the textwidget
        if self.textwidget is not None:
            self.textwidget.configure(font=("Liberation Serif", 12))
        # Add other configurations as needed

    def update_textwidget(self, new_textwidget):
        """Update the internal text widget reference and reapply configurations."""
        self.textwidget = new_textwidget
        self.font_config()  # Reapply configurations to the new text widget


  

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Font Bar Example")
        self.geometry("800x600")

        # Initialize a Text widget
        self.textwidget = tk.Text(self)
        self.textwidget.grid(row=1,column=1)

        # Initialize the FontBar and pass the Text widget to it
        self.font_bar = FontBar(self, self.textwidget)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
