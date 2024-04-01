import tkinter as tk
from tkinter import font
from tkinter import ttk

def update_font_example(*args):
    selected_font = font_combo.get()
    example_label.config(font=(selected_font, 12))
    example_label['text'] = f'This is "{selected_font}" font'

app = tk.Tk()
app.title('Font Viewer')

# Create a combobox to list fonts
font_combo = ttk.Combobox(app, width=50)
font_combo.grid(row=1,column=1)

# Get list of fonts
fonts_list = list(font.families())
fonts_list.sort()
font_combo['values'] = fonts_list

# Create a label to show the example text
example_label = tk.Label(app, text='Example Text', font=('Arial', 12))
example_label.grid(row=1,column=4)

# Bind the combobox selection to the update function
font_combo.bind('<<ComboboxSelected>>', update_font_example)

app.mainloop()

