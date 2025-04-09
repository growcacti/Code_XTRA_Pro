import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor


class WidgetEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter GUI Editor")
        self.bd_var = tk.IntVar(value=1)  # Border width
        self.bg_var = tk.StringVar(value="#ffffff")  # Background color
        self.fg_var = tk.StringVar(value="black")  # Foreground color
        self.width_var = tk.IntVar(value=20)  # Width
        self.height_var = tk.IntVar(value=1)  # Height

        self.create_widgets()

    def create_widgets(self):
        # Frame for widget preview
        preview_frame = ttk.LabelFrame(self.root, text="Widget Preview")
        preview_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.preview_widget = tk.Entry(preview_frame, width=self.width_var.get())
        self.preview_widget.pack(pady=10)

        # Frame for attributes
        attr_frame = ttk.LabelFrame(self.root, text="Edit Attributes")
        attr_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Attribute selectors
        ttk.Label(attr_frame, text="Border Width:").grid(row=0, column=0, sticky="w")
        self.border_spin = tk.Spinbox(
            attr_frame, from_=0, to=20, textvariable=self.bd_var, command=self.update_preview
        )
        self.border_spin.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(attr_frame, text="Background Color:").grid(row=1, column=0, sticky="w")
        self.bg_entry = ttk.Entry(attr_frame, textvariable=self.bg_var)
        self.bg_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(attr_frame, text="Choose Color", command=self.choose_bg_color).grid(row=1, column=2)

        ttk.Label(attr_frame, text="Foreground Color:").grid(row=2, column=0, sticky="w")
        self.fg_entry = ttk.Entry(attr_frame, textvariable=self.fg_var)
        self.fg_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(attr_frame, text="Choose Color", command=self.choose_fg_color).grid(row=2, column=2)

        ttk.Label(attr_frame, text="Width:").grid(row=3, column=0, sticky="w")
        self.width_spin = tk.Spinbox(
            attr_frame, from_=1, to=50, textvariable=self.width_var, command=self.update_preview
        )
        self.width_spin.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(attr_frame, text="Height:").grid(row=4, column=0, sticky="w")
        self.height_spin = tk.Spinbox(
            attr_frame, from_=1, to=10, textvariable=self.height_var, command=self.update_preview
        )
        self.height_spin.grid(row=4, column=1, padx=5, pady=5)

        # Frame for code generation
        code_frame = ttk.LabelFrame(self.root, text="Generated Code")
        code_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.code_text = tk.Text(code_frame, height=10, width=50)
        self.code_text.pack(fill="both", expand=True)

        self.update_preview()

    def choose_bg_color(self):
        color = askcolor()[1]
        if color:
            self.bg_var.set(color)
            self.update_preview()

    def choose_fg_color(self):
        color = askcolor()[1]
        if color:
            self.fg_var.set(color)
            self.update_preview()

    def update_preview(self):
        # Get user-defined values or set defaults
        try:
            bd = self.bd_var.get()
            bg = self.bg_var.get()
            fg = self.fg_var.get()
            width = self.width_var.get()
            height = self.height_var.get()

            self.preview_widget.config(bd=bd, bg=bg, fg=fg, width=width, height=height)
        except Exception as e:
            print(f"Error updating preview: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WidgetEditorApp(root)
    root.mainloop()
