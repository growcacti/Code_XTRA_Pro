import tkinter as tk
import os
import subprocess
import sys
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk


# WIDGETS STRINGS
root = tk.Tk()
root.geometry("900x900")
root.title("TK GUI Generator HPC Engineering")
ecount = 1
btncount = 1
btncount2 = 1
labelcount = 1
canvascount = 1
lboxcount = 1
rowcount = 1
columncount = 1
combocount = 1
spincount = 1
textcount = 1
slidercount = 1
scrollcount = 1
projectcount = 1


start_string = """
#! /usr/bin/python3
# proj_str
root = tk.Tk()
root.title("Tkinter widget helper")

f1 = tk.Frame(root, height=300, width=300)
f1.grid(row=0, rowspan=10, column=5, columnspan=10)
f2 = tk.Frame(root, height=300, width=300)
f2.grid(row=0, column=0, rowspan=5, columnspan=5)
"""


def e_code():
    global ecount, rowcount
    w_str = """
display1 = tk.StringVar()
entry1 = tk.e(root,
    relief=tk.FLAT,
    textvariable=display1,
    justify='right',
    bg='orange')
entry1.grid(row=3, column=4)
entry1["font"] = "arial 12 bold"
    """
    w_str2 = w_str.replace("display1", "display" + str(ecount))
    w_str3 = w_str2.replace("entry1", "entry" + str(ecount))
    w_str4 = w_str3.replace("row=1", "row=" + str(rowcount))
    text.insert(tk.END, w_str4)
    ecount += 1
    rowcount += 1


def button_code1():
    global btncount, rowcount
    w_str = """
b1 = tk.Button(root,
            #relief=tk.FLAT,
            compound=tk.LEFT,
            text="new",
            #command=None,

            )
b1.grid(row=1, column=2)
"""
    w_str2 = w_str.replace("b1", "b" + str(btncount))
    w_str3 = w_str2.replace("row=1", "row=" + str(rowcount))
    text.insert(tk.END, w_str3)
    btncount += 1
    rowcount += 1


def button_code2():
    global btncount2, columncount
    w_str = """
btn1 = tk.Button(root,
            #relief=tk.FLAT,
            compound=tk.LEFT,
            text="new",
            #command=None,

            )
btn1.grid(row=2, column=1)
"""
    w_str2 = w_str.replace("btn1", "btn" + str(btncount2))
    w_str3 = w_str2.replace("column=1", "column=" + str(columncount))
    text.insert(tk.END, w_str3)
    btncount2 += 1
    columncount += 1


def label_code1():
    global labelcount, rowcount
    label_str = """
label1 = tk.Label(root
        ft = tkFont.Font(family='Ariel Black',size=10)
        label1["font"] = ft
        label1["fg"] = "#333333",
        label1["justify"] = "center",
        label1["text"] = "label",
        width=100,height=25)
        label1.grid(row=4, column=2) """
    label_str2 = label_str.replace("label1", "label" + str(labelcount))
    label_str3 = label_str2.replace("row=1", "row=" + str(rowcount))
    text.insert(tk.END, label_str3)
    labelcount += 1
    rowcount += 1


def label_code2():
    global labelcount, columncount
    label_str = """
label1 = tk.Label(root
        ft = tkFont.Font(family='Ariel Black',size=10)
        label1["font"] = ft
        label1["fg"] = "#333333",
        label1["justify"] = "center",
        label1["text"] = "label",
        width=100,height=25)
        label1.grid(row=5, column=2) """
    label_str2 = label_str.replace("label1", "label" + str(labelcount))
    label_str3 = label_str2.replace("column=1", "column=" + str(columncount))
    text.insert(tk.END, label_str3)
    labelcount += 1
    columncount += 1


def listbox_code():
    global lboxcount
    lbox_str = """
lbox1=tk.Listbox(root, width=80, height=25)
    lbox1["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times',size=10)
    lbox1["font"] = ft
    lbox1["fg"] = "#333333"
    lbox1["justify"] = "center"
    lbox1.grid(row=9, coloumn=3)  """
    lbox_str2 = lbox_str.replace("lbox1", "lbox" + str(lboxcount))
    text.insert(tk.END, lbox_str2)
    lboxcount += 1


def menu1_code():
    menu1_str = """
root.option_add('*tearOff',False)
    menubar = Menu(root)
    root.config(menu = menubar)
    File = Menu(menubar)
    Edit = Menu(menubar)
    Help_ = Menu(menubar)
    menubar.add_cascade( menu = File , label = 'File')
    menubar.add_cascade( menu = Edit , label = 'Edit')
    menubar.add_cascade( menu = Help_, label = 'Help')
    File.add_command( label = 'New', command = lambda: print(" New File"))
    File.add_separator()
    File.add_command( label = 'Open',command = lambda: print("Open File"))
    File.add_separator()
    save = Menu(File)
    File.add_cascade( menu = save , label ='Save')
    save.add_command(label ='Save_as', command = lambda: print(" Save as"))
    save.add_command(label ='Save_all',command = lambda: print(" Save all"))
    """
    text.insert(tk.END, menu1_str)


def menu2_code():
    menu2_str = """
    def open():
    messagebox.shorootfo('From My Computer','Your File has been Opened')
    def close():
    messagebox.shorootfo('From My Computer','Your File has been Closed')
    def nothing():
    messagebox.shorootfo('From My Computer','Are You Feeling Well')

    menubar = Menu(root)

    filemenu = Menu(menubar)
    filemenu.add_command(label="Open File",command=open)
    filemenu.add_command(label="New File",command=nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Save",command=nothing)
    filemenu.add_command(label="Save As",command=nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Close",command=close)
    filemenu.add_command(label="Close Tab",command=nothing)
    filemenu.add_command(label="Close rootdow",command=nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit",command=root.quit)

    menubar.add_cascade(label="File", menu = filemenu)

    editmenu = Menu(menubar)
    editmenu.add_command(label="Undo",command=nothing)
    editmenu.add_command(label="Redo",command=nothing)
    editmenu.add_separator()
    editmenu.add_command(label="Copy",command=nothing)
    editmenu.add_command(label="Paste",command=nothing)
    editmenu.add_separator()
    editmenu.add_command(label="Columns",command=nothing)
    editmenu.add_command(label="Lines",command=nothing)
    editmenu.add_command(label="Text",command=nothing)
    editmenu.add_separator()
    editmenu.add_command(label="Exit",command=root.quit)

    menubar.add_cascade(label="Edit", menu = editmenu)

    root.config(menu = menubar)
    """
    text.insert(tk.END, menu2_str)


def canvas_code():
    global canvascount
    canvas_str = """
canvas1 = Canvas(root)
    canvas.grid(row=1, column=1)
    canvas.config(width = 700 , height = 800)

    line = canvas.create_line(40,70, 79,140 , fill ='red', width = 7)

    """

    canvas_str2 = canvas_str.replace("canvas1", "canvas" + str(canvascount))
    text.insert(tk.END, canvas_str2)
    canvascount += 1


def combo_code():
    global combo_str, combocount
    combo_str = """
cbox1 = ttk.Combobox(root, values=["Value1", "value2, "value3"])
cbox1.grid(column=0, row=1)"""
    combo_str2 = combo_str.replace("cbox1", "cbox" + str(combocount))
    text.insert(tk.END, combo_str2)
    combocount += 1


def spin_code():
    global sp, image, img, spincount
    spin_str = """
sp1 = tk.Spinbox(root, from_=1.0, to=1000.0, increment=0.1)
    sp1.grid(row=1, column=0)"""
    spin_str2 = spin_str.replace("sp1", "sp" + str(spincount))
    text.insert(tk.END, spin_str2)
    spincount += 1


def text_code():
    global textcount, spincount
    txt_str = """
txt1 = tk.Text(root, height=60, width=150, bg='white')
txt1.insert('1.0', tk.END)
txt1.grid(row=02
, column=3)"""
    txt_str2 = txt_str.replace("txt1", "txt" + str(txtcount))
    text.insert(tk.END, txt_str2)
    textcount += 1


def slider():
    global txt_str, sld_str

    sld_str = """
slider1 = ttk.Scale(slider_str2 = slidar_str.replace("slider1", "slider" + str(slidercount))
    text.insert(tk.END, slider_str2)
    slidercount += 1"""
    text.insert(tk.END, sld_str)


def scrollbar():
    global txt_str
    # scrollcount not goint to add counter for this yet
    scr_str1 = """
scrollbar = tk.Scrollbar(command=text.yview)
scrollbar.grid(row=0, column=1, sticky='ns')

text['yscrollcommand'] = scrollbar.set
"""
    text.insert(tk.END, scr_str1)


def restartstr():
    text.insert(tk.END, start_string)


def cleartext():
    text.delete("1.0", tk.END)


def open_code():
    # file type
    filetypes = [
        ("Python files", "*.py"),
        ("text files", "*.txt"),
        ("All files", "*.*"),
    ]
    # show the open file dialog
    f = filedialog.askopenfile(filetypes=filetypes)
    # read the text file and show its content on the Text
    text.insert("1.0", f.readlines())


def save_code():
    global text, projectpy, start_string
    stop_str = """
root.mainloop()"""
    text.insert(tk.END, stop_str)
    filetypes = [
        ("Python files", "*.py"),
        ("Text files", "*.txt"),
        ("All files", "*.*"),
    ]

    projectpy = tk.filedialog.asksaveasfilename(
        title="Open a file", initialdir="/home/jh/Desktop", filetypes=filetypes
    )


##def insertfunctions():
##    top = Toplevel()
##    tk.Label(top, text="building functions").grid(row=0, column=0)
##
##    def topf():
##             pass
##
##
##    def opstr():
##        funct_str1="""
##        def open_text_file():
##    # file type
##    filetypes = (
##        ('text files', '*.txt'),
##        ('All files', '*.*')
##    )
##    # show the open file dialog
##    f = fd.askopenfile(filetypes=filetypes)
##    # read the text file and show its content on the Text
##    text.insert('1.0', f.readlines())"""
##    text.insert(tk.END, funct_str1)
##
##
##    def savstr():
##        funct_str2="""
## filetypes = [('Python files', '*.py'), ('Text files', '*.txt'), ('All files', '*.*')]
##
##    projectpy = tk.filedialog.asksaveasfilename(
##        title='Open a file',
##        initialdir='/,
##        filetypes=filetypes)
##    """


##    bbtn1 = tk.Button(top, text="Open File Function", command=opstr)
##    bbtn1.grid(row=1, column=0)
##    bbtn2 = tk.Button(top, text="Save File Function", command=savstr)
##    bbtn2.grid(row=2, column=0)
##    bbtn3 = tk.Button(top, text="", command=topf)
##    bbtn3.grid(row=4, column=0)
##    bbtn4 = tk.Button(top, text="  ", command=topf)
##    bbtn4.grid(row=5, column=0)
##    bbtn5 = tk.Button(top, text="  ", command=topf)
##    bbtn5.grid(row=6, column=0)
##    bbtn6 = tk.Button(top, text=" ", command=topf)
##    bbtn6.grid(row=7, column=0)
##    bbtn7 = tk.Button(top, text=" ", command=topf)
##    bbtn7.grid(row=8, column=0)
##    bbtn8 = tk.Button(top, text="  ", command=save_co)
##    bbtn9.grid(row=9, column=0)
##
##


f1 = tk.Frame(root, height=300, width=300)
f1.grid(row=0, rowspan=4, column=0, columnspan=2)
f2 = tk.Frame(root, height=300, width=300)
f2.grid(row=3, column=3, rowspan=5, columnspan=5)
text = tk.Text(f2, height=60, width=100)
text.grid(row=1, column=3)
text.insert(tk.END, start_string)
b1 = tk.Button(f1, text="Entry Widget", command=e_code)
b1.grid(row=2, column=0)
b2 = tk.Button(f1, text="Insert Button row", command=button_code1)
b2.grid(row=3, column=0)
b55 = tk.Button(f1, text="Insert Button column", command=button_code2)
b55.grid(row=4, column=0)
b4 = tk.Button(f1, text="Insert label row", command=label_code1)
b4.grid(row=5, column=0)
b5 = tk.Button(f1, text="List Box", command=listbox_code)
b5.grid(row=6, column=0)
b6 = tk.Button(f1, text="Menu1", command=menu1_code)
b6.grid(row=7, column=0)
b7 = tk.Button(f1, text="Menu2", command=menu2_code)
b7.grid(row=8, column=0)
b8 = tk.Button(f1, text="Canvas", command=canvas_code)
b8.grid(row=9, column=0)
b9 = tk.Button(f1, text="Combobox", command=combo_code)
b9.grid(row=10, column=0)
bba = tk.Button(f1, text="Spinbox", command=spin_code)
bba.grid(row=11, column=0)
bb1 = tk.Button(f1, text="Text Box", command=text_code)
bb1.grid(row=12, column=0)
b14 = tk.Button(f1, text="insert label col", command=label_code2)
b14.grid(row=14, column=0)
b15 = tk.Button(f1, text="Slider Widget", command=slider)
b15.grid(row=15, column=0)
b16 = tk.Button(f1, text="Scroll Bar", command=scrollbar)
b16.grid(row=16, column=0)
b17 = tk.Button(f1, text="Clear Code Box", command=cleartext)
b17.grid(row=17, column=0)
b18 = tk.Button(f1, text="Restart 1st Code Block", command=restartstr)
b18.grid(row=18, column=0)
b19 = tk.Button(f1, text="Finish & Save", command=save_code)
b19.grid(row=19, column=0)
b20 = tk.Button(f1, text="Open File", command=open_code)
b20.grid(row=20, column=0)
root.mainloop()


#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################


#######################################################################################
#######################################################################################
###
###   Original code with run fix cross platform
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################

####import tkinter as tk
##from tkinter import *
##import os
##import subprocess
##import sys
##
### WIDGETS STRINGS
##
##
##
##
##
##entry_counter = 1
##
##button_counter = 1
##
##lbcount = 1
##
##labelcount = 1
##
##cbcount = 1
##
##def entry_code():
##
##    global entry_counter
##
##    w_string = """
##
##display1 = tk.StringVar()
##
##entry1 = tk.Entry(root,
##
##    relief=tk.FLAT,
##
##    textvariable=display1,
##
##    justify='right',
##
##    bg='orange')
##
##entry1.pack()
##
##entry1["font"] = "Arial Black 12 bold"
##
##    """
##
##    w_string2 = w_string.replace("display1", "display" + str(entry_counter))
##
##    w_string2 = w_string2.replace("entry1", "entry" +  str(entry_counter))
##
##    text.insert(tk.END, w_string2)
##
##    entry_counter += 1
##
##
##
##def button_code():
##
##    global button_counter
##
##    w_string = """
##
##b1 = tk.Button(root,
##
##            #relief=tk.FLAT,
##
##            compound=tk.LEFT,
##
##            text="new",
##
##            #command=None,
##
##            #image=tk.PhotoImage("img.png")
##
##            )
##
##b1.pack()
##
##"""
##
##    w_string2 = w_string.replace("b1", "b" + str(button_counter))
##
##    text.insert(tk.END, w_string2)
##
##    button_counter += 1
##
##
##
##def label_code():
##
##    global labelcount
##
##    w_str = """ label1 = tk.Label(root)
##
##
##
##
##
##        label1["font"] = "Arial Black 12 bold"
##
##        label1["fg"] = "#333333",
##
##        label1["justify"] = "center",
##
##        label1["text"] = "label",
##
##        width=100,height=25)
##
##        label1.pack()"""
##
##    w_str2 = w_str.replace("label1", "label" + str(labelcount))
##
##    text.insert(tk.END, w_str2)
##
##    labelcount += 1
##
##
##
##def listbox_code():
##
##     global lbcount
##
##     w_str = """ lbox1=tk.Listbox(root, width=80, height=25)
##
##        lbox1["borderwidth"] = "1px"
##
##        ft = tkFont.Font(family='Times',size=10)
##
##
##
##        lbox1["fg"] = "#333333"
##
##        lbox1["justify"] = "center"
##
##        lbox1.pack()"""
##
##def combobox_code():
##
##    global cbcount
##
##    w_str = """ lbox1=tk.Listbox(root, width=80, height=25)
##
##        lbox1["borderwidth"] = "1px"
##
##
##
##
##
##        lbox1["fg"] = "#333333"
##
##        lbox1["justify"] = "center"
##
##        lbox1.pack()  """
##


##
##root = tk.Tk()
##
##root.title("Tkinter widget helper")
##
##f1 = tk.Frame(root)
##
##f1.pack(side="left")
##
##b1 = tk.Button(f1, text="entry", command=entry_code)
##
##b1.pack()
##
##
##
##
##
##b2 = tk.Button(f1, text="button", command=button_code)
##
##b2.pack()
##
##
##
##b3 = tk.Button(f1, text="save", command=save_code)
##
##b3.pack()
##
##
##
##b4 = tk.Button(f1, text="insert label", command=label_code)
##
##b4.pack()
##
##b5 = tk.Button(f1, text="list box", command=listbox_code)
##
##b5.pack()
##
##
##
##f2 = tk.Frame(root)
##
##f2.pack(side="left")
##
##text = tk.Text(f2)
##
##text.pack()
##
##start_string = """# project.py
##
##import tkinter as tk
##
##from tkinter import ttk
##
##from tkinter import simpledialog
##
##from tkinter import messagebox
##
##from tkinter import *
##
##root = tk.Tk()
##
##"""
##
##text.insert("0.0", start_string)
##
##
##
##root.mainloop()
