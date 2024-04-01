import tkinter as tk

class TextWidgetInfo:
    def __init__(self, parent, textwidget):
        self.parent = parent
        self.tx = textwidget
        self.info_label = tk.Label(self.parent, text="Lines: 0  \n | Words: 0   \n| Characters: 0 \n| Cursor Position: Line 1   , Column 0       ")
        self.info_label.grid(row=30, column=0)

        # Bind to text change and cursor movement events
        self.tx.bind("<KeyRelease>", self.update_info)
        self.tx.bind("<ButtonRelease-1>", self.update_info)
        self.tx.bind("<<Modified>>", self.on_text_modified)
        self.tx.bind("<ButtonRelease-2>", self.update_info)
    def on_text_modified(self, event):
        if self.tx.edit_modified():
            self.update_info(event)
            self.tx.edit_modified(False)

    def update_info(self, event=None):
        # Get the current text content
        content = self.tx.get("1.0", "end-1c")

        # Count the lines, words, and characters
        lines = self.tx.index("end-1c").split(".")[0]
        words = len(content.split())
        characters = len(content)

        # Get the current cursor position (line and column)
        cursor_position = self.tx.index("insert")
        cursor_line, cursor_column = cursor_position.split(".")

        # Update the label with the new information
        self.info_label.config(
            text=f"Lines: {lines}   \n| Words: {words}       \n| Characters: {characters}     \n | Cursor Position: Line {cursor_line}, Column {cursor_column}"
        )
