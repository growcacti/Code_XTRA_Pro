import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk
import re


def remove_add(parent):

    def remove_lines():
        interval = int(interval_spinbox.get())  # Get the interval from the Spinbox
        text_content = input_text_box.get("1.0", "end-1c").split('\n')
        # Modify the logic to work with the selected interval
        new_text_content = '\n'.join(line if i % interval != 0 else '' for i, line in enumerate(text_content, start=1))
        output_text_box.delete("1.0", "end")
        output_text_box.insert("1.0", new_text_content)

    def remove_every_other_line():
        text_content = input_text_box.get("1.0", "end-1c").split('\n')
        new_text_content = '\n'.join(line for i, line in enumerate(text_content) if i % 2 == 0)
        output_text_box.delete("1.0", "end")
        output_text_box.delete("1.0", new_text_content)

    def remove_line_numbers():
        text = input_text_box.get("1.0", tk.END)
        pattern = r'^\s*\d+\s+'
        cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
        output_text_box.delete("1.0", tk.END)
        output_text_box.insert(tk.END, cleaned_text)

    def clear_text():
        input_text_box.delete("1.0", tk.END)
        output_text_box.delete("1.0", tk.END)

    def load_text():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                input_text_box.delete("1.0", tk.END)
                input_text_box.insert(tk.END, text)

    def save_text():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            text = output_text_box.get("1.0", tk.END)
            with open(file_path, 'w') as file:
                file.write(text)

        # Setting up the GUI window



    # Creating and placing the text input and output boxes
    input_text_box = scrolledtext.ScrolledText(parent, width=40, height=10)
    input_text_box.grid(row=0, column=0, padx=10, pady=10)
    output_text_box = scrolledtext.ScrolledText(parent, width=40, height=10)
    output_text_box.grid(row=0, column=1, padx=10, pady=10)

    # Creating and placing the operation buttons
    remove_button = tk.Button(parent, text="Remove Line Numbers", command=remove_line_numbers)
    remove_button.grid(row=1, column=0, pady=10)
    remove_line_btn = tk.Button(parent, text="Remove Every Other Line", command=remove_every_other_line)
    remove_line_btn.grid(row=2,column=0)


    remove_lines_btn = tk.Button(parent, text="Remove Every # Lines", command=remove_lines)
    remove_lines_btn.grid(row=3,column=0)
    clear_button = tk.Button(parent, text="Clear Text", command=clear_text)
    clear_button.grid(row=1, column=1, pady=10)
    load_button = tk.Button(parent, text="Load Text", command=load_text)
    load_button.grid(row=2, column=1, pady=10)
    save_button = tk.Button(parent, text="Save Text", command=save_text)
    save_button.grid(row=3, column=1, pady=10)

    interval_label = tk.Label(parent, text="Interval:")
    interval_label.grid(row=1, column=2, sticky='w', padx=5)
    interval_spinbox = tk.Spinbox(parent, from_=1, to=10, width=5)
    interval_spinbox.grid(row=1, column=3, sticky='w', padx=5)   






























"""Features Explained:

    Remove Line Numbers: Removes line numbers from the input text and displays the result in the output box.
    Clear Text: Clears both input and output text boxes.
    Load Text: Opens a dialog to select a text file and loads its content into the input text box.
    Save Text: Opens a dialog to save the content of the output text box to a file.

👉 Next Steps: Copy this updated code into a file named remove_line_numbers_gui.py and run it.
You'll now have the ability to clear text, as well as load and save files directly from the GUI.

"""
