import tkinter.simpledialog as simpledialog
import re

def remove_after(self):
    delimiter = simpledialog.askstring("Input", "Enter the delimiter or pattern:")
    use_regex = simpledialog.askstring("Input", "Use regex? (yes/no):")
    if delimiter:
        current_text = self.textwidget.get("1.0", tk.END)
        if use_regex.lower() == 'yes':
            pattern = re.escape(delimiter) + ".*"
            modified_text = re.sub(pattern, '', current_text, flags=re.DOTALL)
        else:
            modified_text = current_text.split(delimiter, 1)[0]
        self.textwidget.delete("1.0", tk.END)
        self.textwidget.insert("1.0", modified_text)

def remove_before(self):
    # Similar to remove_after but adjusts the logic to remove text before the delimiter
self.format_menu.add_command(label="Remove After...", command=self.remove_after)
self.format_menu.add_command(label="Remove Before...", command=self.remove_before)



def remove_after(self):
    pattern = simpledialog.askstring("Input", "Remove everything after (inclusive):")
    if not pattern:
        return  # User cancelled or empty input

    content = self.textwidget.get("1.0", tk.END)
    index = content.find(pattern)
    if index != -1:
        self.textwidget.delete(f"1.0+{index}c", tk.END)
    else:
        messagebox.showinfo("Info", "Pattern not found.")

def remove_before(self):
    pattern = simpledialog.askstring("Input", "Remove everything before (inclusive):")
    if not pattern:
        return  # User cancelled or empty input

    content = self.textwidget.get("1.0", tk.END)
    index = content.rfind(pattern)
    if index != -1:
        self.textwidget.delete("1.0", f"1.0+{index+len(pattern)}c")
    else:
        messagebox.showinfo("Info", "Pattern not found.")








import re

def remove_after_regex(self):
    pattern = simpledialog.askstring("Input", "Regex pattern to remove everything after:")
    if not pattern:
        return  # User cancelled or empty input

    content = self.textwidget.get("1.0", tk.END)
    modified_content = re.split(pattern, content, maxsplit=1)[0]
    self.textwidget.delete("1.0", tk.END)
    self.textwidget.insert("1.0", modified_content)



def remove_after_char(text, char):
    return text.split(char)[0]

import re

def remove_after_char_regex(text, char):
    pattern = re.escape(char) + ".*"
    return re.sub(pattern, '', text, count=1)




class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Assuming you have already setup other menu items
        # Adding a new menu for text manipulation
        text_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Text", menu=text_menu)
        
        # Adding options to the text menu
        text_menu.add_command(label="Remove after character", command=self.remove_after_character_ui)
    
    def remove_after_character_ui(self):
        # This method can be called when the menu item is clicked.
        # You can use simpledialog to ask the user for the character
        char = tk.simpledialog.askstring("Input", "Enter character after which text should be removed:")
        if char:
            current_text = self.parent.text_widget.get("1.0", tk.END)  # Assuming you have a reference to the text widget
            new_text = remove_after_char_regex(current_text, char)
            self.parent.text_widget.delete("1.0", tk.END)
            self.parent.text_widget.insert(tk.END, new_text)


self.edit_menu.add_command(label="Remove After", command=self.remove_after)
self.edit_menu.add_command(label="Remove Before", command=self.remove_before)


import tkinter.simpledialog as simpledialog
import re

def remove_after(self):
    delimiter = simpledialog.askstring("Input", "Enter the delimiter or pattern:")
    use_regex = simpledialog.askstring("Input", "Use regex? (yes/no):")
    if delimiter:
        current_text = self.textwidget.get("1.0", tk.END)
        if use_regex.lower() == 'yes':
            pattern = re.escape(delimiter) + ".*"
            modified_text = re.sub(pattern, '', current_text, flags=re.DOTALL)
        else:
            modified_text = current_text.split(delimiter, 1)[0]
        self.textwidget.delete("1.0", tk.END)
        self.textwidget.insert("1.0", modified_text)

def remove_before(self):
    delimiter = simpledialog.askstring("Input", "Enter the delimiter or pattern:")
    use_regex = simpledialog.askstring("Input", "Use regex? (yes/no):")
    if delimiter:
        current_text = self.textwidget.get("1.0", tk.END)
        if use_regex.lower() == 'yes':
            # Regex to capture everything after the delimiter
            pattern = re.escape(delimiter) + "(.*)"
            matches = re.search(pattern, current_text, flags=re.DOTALL)
            modified_text = matches.group(1) if matches else ""
        else:
            # Split the text and take the part after the delimiter, if present
            parts = current_text.split(delimiter, 1)
            modified_text = parts[1] if len(parts) > 1 else ""
        self.textwidget.delete("1.0", tk.END)
        self.textwidget.insert("1.0", modified_text)

def remove_before_each_line(self):
    delimiter = simpledialog.askstring("Input", "Enter the delimiter or pattern:")
    use_regex = simpledialog.askstring("Input", "Use regex? (yes/no):").lower() == 'yes'
    
    current_text = self.textwidget.get("1.0", tk.END)
    modified_lines = []

    for line in current_text.splitlines():
        if use_regex:
            pattern = ".*" + re.escape(delimiter)
            match = re.search(pattern, line)
            modified_line = line[match.end():] if match else line
        else:
            parts = line.split(delimiter, 1)
            modified_line = parts[1] if len(parts) > 1 else line
        modified_lines.append(modified_line)

    self.textwidget.delete("1.0", tk.END)
    self.textwidget.insert("1.0", "\n".join(modified_lines))

    def remove_after_each_line(self):
    delimiter = simpledialog.askstring("Input", "Enter the delimiter or pattern:")
    use_regex = simpledialog.askstring("Input", "Use regex? (yes/no):").lower() == 'yes'
    
    current_text = self.textwidget.get("1.0", tk.END)
    modified_lines = []

    for line in current_text.splitlines():
        if use_regex:
            pattern = re.escape(delimiter) + ".*"
            modified_line = re.sub(pattern, '', line)
        else:
            modified_line = line.split(delimiter, 1)[0] if delimiter in line else line
        modified_lines.append(modified_line)

    self.textwidget.delete("1.0", tk.END)
    self.textwidget.insert("1.0", "\n".join(modified_lines))


     def alternate_modification_ui(self):
        # Prompt the user for the character
        char = simpledialog.askstring("Input", "Enter character for alternation:")
        if char:
            current_text = self.parent.text_widget.get("1.0", tk.END)  # Assuming a reference to the text widget
            new_text = alternate_lines(current_text, char)
            self.parent.text_widget.delete("1.0", tk.END)
            self.parent.text_widget.insert(tk.END, new_text)

import re

def remove_after_each_line_regex(self):
    pattern = simpledialog.askstring("Input", "Regex pattern to remove everything after (inclusive):")
    if not pattern:
        return  # User cancelled or empty input

    content = self.textwidget.get("1.0", tk.END)
    lines = content.splitlines()
    modified_content = ""
    for line in lines:
        new_line = re.split(pattern, line, maxsplit=1)[0]
        modified_content += f"{line}\n{new_line}\n"
    
    self.textwidget.delete("1.0", tk.END)
    self.textwidget.insert("1.0", modified_content)

def remove_before_each_line_regex(self):
    pattern = simpledialog.askstring("Input", "Regex pattern to remove everything before (inclusive):")
    if not pattern:
        return  # User cancelled or empty input

    content = self.textwidget.get("1.0", tk.END)
    lines = content.splitlines()
    modified_content = ""
    for line in lines:
        matches = list(re.finditer(pattern, line))
        if matches:
            index = matches[-1].end()
            new_line = line[index:]
        else:
            new_line = line
        modified_content += f"{line}\n{new_line}\n"
    
    self.textwidget.delete("1.0", tk.END)
    self.textwidget.insert("1.0", modified_content)
