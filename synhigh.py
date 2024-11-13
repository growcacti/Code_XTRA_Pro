import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import re

class SyntaxHighlite:
    def __init__(self,textwidget):
        self.textwidget = textwidget
        self.syntax_elements = {
            'comment': r'#[^\n]*|(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\")',
            'number': r'\b\d+(\.\d+)?\b',
            'string': r'".*?"|\'.*?\'',
            'keyword': r'\b(import|as|pass|return|def|if|else|elif|for|while|break|continue|try|except|finally|with|as|in|not|and|or|is|None|True|False)\b',
            'classes': r'\b(@static_method|class|@property|@class_method|self|super|cls)\b',}
        self.configure_tags()

        # Trigger syntax highlighting after any key is pressed
        self.textwidget.bind('<KeyRelease>', self.highlight_syntax)

    def configure_tags(self):
        self.textwidget.tag_config('keyword', foreground='orangered')
        self.textwidget.tag_config('string', foreground='cyan')
        self.textwidget.tag_config('comment', foreground='red')
        self.textwidget.tag_config('number', foreground='lawngreen')
        self.textwidget.tag_config('classes', foreground='deep pink')
    def highlight_syntax(self, event=None):
        for tag in self.syntax_elements.keys():
            self.textwidget.tag_remove(tag, '1.0', tk.END)

        for tag, pattern in self.syntax_elements.items():
            start_index = '1.0'
            while True:
                match = re.search(pattern, self.textwidget.get(start_index, tk.END), re.MULTILINE)
                if not match: break
                start_index = self.textwidget.index(f"{start_index}+{match.start()}c")
                end_index = self.textwidget.index(f"{start_index}+{match.end() - match.start()}c")
                self.textwidget.tag_add(tag, start_index, end_index)
                start_index = end_index
##
##root=tk.Tk()
##textwidget = ScrolledText(root)
##textwidget.grid(row=0,column=0)
##syn = SyntaxHighlite(textwidget)
