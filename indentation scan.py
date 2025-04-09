import tkinter as tk
from tkinter import filedialog, messagebox


def analyze_indentation():
    """Scan the file and show indentation for each line in the Text widget."""
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        text_widget.delete("1.0", tk.END)  # Clear previous content
        for i, line in enumerate(lines, start=1):
            spaces = len(line) - len(line.lstrip(' '))
            text_widget.insert(tk.END, f"Line {i}: {spaces} spaces\n")

        messagebox.showinfo("Success", "File analyzed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze the file: {e}")


def save_output():
    """Save the content of the Text widget to a file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not file_path:
        return

    try:
        with open(file_path, 'w') as file:
            content = text_widget.get("1.0", tk.END).strip()
            file.write(content)
        messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the file: {e}")


# Create the main application window
root = tk.Tk()
root.title("Python Indentation Analyzer")

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Add buttons to load and save files
load_button = tk.Button(button_frame, text="Analyze File", command=analyze_indentation)
load_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(button_frame, text="Save Output", command=save_output)
save_button.grid(row=0, column=1, padx=5)

# Create a Text widget to display the results
text_widget = tk.Text(root, wrap=tk.NONE, height=20, width=60)
text_widget.pack(padx=10, pady=10)

# Add scrollbars to the Text widget
scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=text_widget.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=text_widget.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# Start the main event loop
root.mainloop()
