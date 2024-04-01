import tkinter as tk
from tkinter import font
from tkinter import ttk

def update_font_example(event):
    selected_font = font_listbox.get(font_listbox.curselection())
    example_label.config(font=(selected_font, 12))
    example_label['text'] = f'This is "{selected_font}" font'

app = tk.Tk()
app.title('Font Viewer')

# Create a scrollbar
scrollbar = tk.Scrollbar(app)
scrollbar.grid(row=0, column=1, sticky='ns')

# Create a listbox to list fonts
font_listbox = tk.Listbox(app, width=50, yscrollcommand=scrollbar.set)
font_listbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Configure the scrollbar
scrollbar.config(command=font_listbox.yview)

# Get list of fonts and insert into the listbox
fonts_list = list(font.families())
fonts_list.sort()
for f in fonts_list:
    font_listbox.insert(tk.END, f)

# Create a label to show the example text
example_label = tk.Label(app, text='Example Text', font=('Arial', 12))
example_label.grid(row=1, column=0, padx=10, pady=20, columnspan=2)

# Bind the listbox selection to the update function
font_listbox.bind('<<ListboxSelect>>', update_font_example)

app.mainloop()
