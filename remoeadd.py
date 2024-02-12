import tkinter as tk
from tkinter import scrolledtext, filedialog, Spinbox
import re

def remove_line_numbers(parent):
    def remove_every_other_line():
        interval = int(interval_spinbox.get())  # Get the interval from the Spinbox
        text_content = input_text_box.get("1.0", "end-1c").split('\n')
        # Modify the logic to work with the selected interval
        new_text_content = '\n'.join(line if i % interval != 0 else '' for i, line in enumerate(text_content, start=1))
        output_text_box.delete("1.0", "end")
        output_text_box.insert("1.0", new_text_content)

    # Correction for remove_line_numbers here as per your original intent

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

    # Spinbox for selecting the interval
    interval_label = tk.Label(parent, text="Interval:")
    interval_label.grid(row=1, column=2, sticky='w', padx=5)
    interval_spinbox = Spinbox(parent, from_=1, to=10, width=5)
    interval_spinbox.grid(row=1, column=3, sticky='w', padx=5)

    # Your existing setup for input_text_box, output_text_box, and buttons continues here

    # Ensure to place the new Spinbox and its label correctly within your grid layout
    # Adjust the row and column indices as necessary to fit your UI layout

# Remember to initialize the Tkinter application and call the function with the root as the argument
if __name__ == "__main__":
    root = tk.Tk()
    remove_line_numbers(root)
    root.mainloop()
