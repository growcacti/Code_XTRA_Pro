import tkinter as tk
from tkinter import filedialog, messagebox
import os

class IndentFixerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Indentation Fixer")

        # Text widget
        self.text = tk.Text(root, wrap='none', font=('Courier', 11), undo=True)
        self.text.grid(row=0, column=0, columnspan=6, sticky='nsew')

        # Scrollbars
        x_scroll = tk.Scrollbar(root, orient='horizontal', command=self.text.xview)
        y_scroll = tk.Scrollbar(root, orient='vertical', command=self.text.yview)
        self.text.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        x_scroll.grid(row=1, column=0, columnspan=6, sticky='ew')
        y_scroll.grid(row=0, column=6, sticky='ns')

        # Options
        self.var_8to4 = tk.BooleanVar(value=True)
        self.var_tabs_to_spaces = tk.BooleanVar()
        self.var_spaces_to_tabs = tk.BooleanVar()

        tk.Checkbutton(root, text="8 → 4 Spaces", variable=self.var_8to4).grid(row=2, column=0, sticky='w')
        tk.Checkbutton(root, text="Tabs → 4 Spaces", variable=self.var_tabs_to_spaces).grid(row=2, column=1, sticky='w')
        tk.Checkbutton(root, text="4 Spaces → Tabs", variable=self.var_spaces_to_tabs).grid(row=2, column=2, sticky='w')

        # Buttons
        tk.Button(root, text="Load File", command=self.load_file).grid(row=3, column=0, sticky='ew')
        tk.Button(root, text="Save File", command=self.save_file).grid(row=3, column=1, sticky='ew')
        tk.Button(root, text="Fix Indent", command=self.fix_indentation).grid(row=3, column=2, sticky='ew')
        tk.Button(root, text="Process Folder", command=self.process_directory).grid(row=3, column=3, sticky='ew')
        tk.Button(root, text="Clear", command=self.clear_text).grid(row=3, column=4, sticky='ew')
        tk.Button(root, text="Exit", command=root.quit).grid(row=3, column=5, sticky='ew')

        # Layout behavior
        root.grid_rowconfigure(0, weight=1)
        for col in range(6):
            root.grid_columnconfigure(col, weight=1)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if path:
            with open(path, 'r') as file:
                content = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.root.title(f"Python Indentation Fixer - {os.path.basename(path)}")

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".py",
                                            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if path:
            with open(path, 'w') as file:
                file.write(self.text.get("1.0", tk.END).rstrip('\n'))
            messagebox.showinfo("Saved", f"File saved to:\n{path}")

    def clear_text(self):
        self.text.delete("1.0", tk.END)

    def fix_indentation(self):
        content = self.text.get("1.0", tk.END)
        fixed_lines = []
        for line in content.splitlines():
            if self.var_8to4.get():
                line = self.convert_8_to_4_spaces(line)
            if self.var_tabs_to_spaces.get():
                line = self.convert_tabs_to_spaces(line)
            if self.var_spaces_to_tabs.get():
                line = self.convert_spaces_to_tabs(line)
            fixed_lines.append(line)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, '\n'.join(fixed_lines))

    def convert_tabs_to_spaces(self, line, tab_size=4):
        return line.replace('\t', ' ' * tab_size)
    def convert_8_to_4_spaces(self, line):
        leading_spaces = len(line) - len(line.lstrip(' '))
        fixed_spaces = 0

        # Replace all full 8-space blocks
        while leading_spaces >= 8:
            fixed_spaces += 4
            leading_spaces -= 8

        # Add back any leftover smaller indents (like 4 or 2 spaces)
        fixed_spaces += leading_spaces

        return ' ' * fixed_spaces + line.lstrip(' ')






    def convert_spaces_to_tabs(self, line, space_size=4):
        return line.replace(' ' * space_size, '\t')

    def process_directory(self):
        dir_path = filedialog.askdirectory()
        if not dir_path:
            return

        confirm = messagebox.askyesno("Process Directory",
            f"Are you sure you want to process all .py files in:\n\n{dir_path}\n\nThis will overwrite files.")
        if not confirm:
            return

        modified = 0
        for root_dir, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root_dir, file)
                    with open(full_path, 'r') as f:
                        lines = f.read().splitlines()
                    new_lines = []
                    changed = False
                    for line in lines:
                        original = line
                        if self.var_8to4.get():
                            line = self.convert_8_to_4_spaces(line)
                        if self.var_tabs_to_spaces.get():
                            line = self.convert_tabs_to_spaces(line)
                        if self.var_spaces_to_tabs.get():
                            line = self.convert_spaces_to_tabs(line)
                        if line != original:
                            changed = True
                        new_lines.append(line)
                    if changed:
                        with open(full_path, 'w') as f:
                            f.write('\n'.join(new_lines))
                        modified += 1

        messagebox.showinfo("Done", f"Processed {modified} file(s) in:\n{dir_path}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = IndentFixerApp(root)
    root.mainloop()
