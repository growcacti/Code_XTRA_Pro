import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import autopep8
from black import format_file_contents, FileMode, NothingChanged
from pylint.lint import Run
from io import StringIO

class CodeFormatterApp:
    def __init__(self, root):
        self.root = root
              
        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid expansion
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # Create tabs
        self._create_original_code_tab()
        self._create_formatted_code_tab()
        self._create_linter_output_tab()
        
        # Track the original file path
        self.original_file_path = None
    
    def _create_original_code_tab(self):
        """Create the Original Code tab."""
        tab_original = ttk.Frame(self.notebook)
        self.notebook.add(tab_original, text="Original Code")
        
        tab_original.rowconfigure(0, weight=1)
        tab_original.columnconfigure(0, weight=1)
        
        self.text_original = tk.Text(tab_original, wrap="word")
        self.text_original.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        btn_load = tk.Button(tab_original, text="Load Code", command=self.load_file)
        btn_load.grid(row=1, column=0, pady=5)

    def _create_formatted_code_tab(self):
        """Create the Formatted Code tab."""
        tab_formatted = ttk.Frame(self.notebook)
        self.notebook.add(tab_formatted, text="Formatted Code")
        
        tab_formatted.rowconfigure(0, weight=1)
        tab_formatted.columnconfigure(0, weight=1)
        
        self.text_formatted = tk.Text(tab_formatted, wrap="word", state="normal")
        self.text_formatted.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        btn_black = tk.Button(tab_formatted, text="Format with Black", command=self.format_with_black)
        btn_black.grid(row=1, column=0, padx=5, pady=5)
        
        btn_autopep8 = tk.Button(tab_formatted, text="Format with Autopep8", command=self.format_with_autopep8)
        btn_autopep8.grid(row=1, column=1, padx=5, pady=5)
        
        btn_save = tk.Button(tab_formatted, text="Save Code", command=self.save_formatted_code)
        btn_save.grid(row=2, column=0, columnspan=2, pady=5)

    def _create_linter_output_tab(self):
        """Create the Linter Output tab."""
        tab_linter = ttk.Frame(self.notebook)
        self.notebook.add(tab_linter, text="Linter Output")
        
        tab_linter.rowconfigure(0, weight=1)
        tab_linter.columnconfigure(0, weight=1)
        
        self.text_linter = tk.Text(tab_linter, wrap="word", state="normal")
        self.text_linter.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        btn_lint = tk.Button(tab_linter, text="Run Linter", command=self.run_linter)
        btn_lint.grid(row=1, column=0, pady=5)

    def load_file(self):
        """Load a Python file into the Original Code tab."""
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.original_file_path = file_path
            with open(file_path, "r") as file:
                self.text_original.delete("1.0", tk.END)
                self.text_original.insert("1.0", file.read())

    def format_with_black(self):
        """Format code using Black and display it in the Formatted Code tab."""
        self._update_output(self.text_original, self.text_formatted, self._format_with_black)

    def format_with_autopep8(self):
        """Format code using Autopep8 and display it in the Formatted Code tab."""
        self._update_output(self.text_original, self.text_formatted, self._format_with_autopep8)

    def run_linter(self):
        """Run a linter on the code and display the output in the Linter Output tab."""
        self._update_output(self.text_original, self.text_linter, self._lint_code)

    def save_formatted_code(self):
        """Save the formatted code to a file with a unique name."""
        formatted_code = self.text_formatted.get("1.0", tk.END).strip()
        if not formatted_code:
            messagebox.showerror("Error", "No formatted code to save!")
            return
        
        # Determine save path
        if self.original_file_path:
            base_name = self.original_file_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        else:
            base_name = "formatted_code"
        unique_filename = f"{base_name}_{int(time.time())}.py"
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            initialfile=unique_filename,
            filetypes=[("Python Files", "*.py")]
        )
        
        if save_path:
            with open(save_path, "w") as file:
                file.write(formatted_code)
            messagebox.showinfo("Success", f"Formatted code saved to {save_path}!")

    def _update_output(self, input_text, output_text, processor):
        """Update the output tab with processed results."""
        original_code = input_text.get("1.0", tk.END).strip()
        if not original_code:
            messagebox.showerror("Error", "No code to process!")
            return
        try:
            result = processor(original_code)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _format_with_black(self, code):
        """Format code using Black."""
        try:
            formatted_code = format_file_contents(code, fast=True, mode=FileMode())
            return formatted_code
        except NothingChanged:
            return "No changes needed, code is already formatted."
        except Exception as e:
            return str(e)

    def _format_with_autopep8(self, code):
        """Format code using Autopep8."""
        return autopep8.fix_code(code)

    def _lint_code(self, code):
        """Run a linter (pylint) on the code."""
        pylint_output = StringIO()
        try:
            Run(['--from-stdin'], do_exit=False, stdout=pylint_output, stdin=StringIO(code))
            return pylint_output.getvalue()
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeFormatterApp(root)
    root.title("Code Formatter and Linter")
    root.mainloop()
