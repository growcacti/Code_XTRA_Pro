import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import random

class RandomTupleGeneratorApp:
    def __init__(self, parent):

      
    
        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Number of tuples
        ttk.Label(frame, text="Number of tuples:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.num_tuples_entry = ttk.Entry(frame)
        self.num_tuples_entry.grid(column=1, row=0, pady=5)
        self.num_tuples_entry.insert(0, "5")

        # Tuple size
        ttk.Label(frame, text="Size of each tuple:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.tuple_size_entry = ttk.Entry(frame)
        self.tuple_size_entry.grid(column=1, row=1, pady=5)
        self.tuple_size_entry.insert(0, "3")

        # Range start
        ttk.Label(frame, text="Start range:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.start_range_entry = ttk.Entry(frame)
        self.start_range_entry.grid(column=1, row=2, pady=5)
        self.start_range_entry.insert(0, "1")

        # Range end
        ttk.Label(frame, text="End range:").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.end_range_entry = ttk.Entry(frame)
        self.end_range_entry.grid(column=1, row=3, pady=5)
        self.end_range_entry.insert(0, "10")

        # Generate button
        generate_btn = ttk.Button(frame, text="Generate", command=self.generate_random_tuples)
        generate_btn.grid(column=0, row=4, columnspan=2, pady=10)

        # Save to file button
        save_btn = ttk.Button(frame, text="Save to File", command=self.save_to_file)
        save_btn.grid(column=0, row=5, columnspan=2, pady=10)

        # Result display
        self.result_text = scrolledtext.ScrolledText(frame, height=10, width=50)
        self.result_text.grid(column=0, row=6, columnspan=2, pady=5)

        # Copy to clipboard button
        copy_btn = ttk.Button(frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.grid(column=0, row=7, columnspan=2, pady=10)

    def generate_random_tuples(self):
        n = int(self.num_tuples_entry.get())
        tuple_size = int(self.tuple_size_entry.get())
        start_range = int(self.start_range_entry.get())
        end_range = int(self.end_range_entry.get())

        result = [tuple(random.randint(start_range, end_range) for _ in range(tuple_size)) for _ in range(n)]
        self.result_text.insert("1.0", str(result))
        return result

    def save_to_file(self):
        tuples = self.generate_random_tuples()
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w') as f:
                for t in tuples:
                    f.write(str(t) + "\n")

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.result_text.get('1.0', tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTupleGeneratorApp(root)
    root.mainloop()
