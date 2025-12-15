# src/pynote/editor.py
"""
Editor widget wrapper for PyNote.
"""

import tkinter as tk
from tkinter import ttk


class EditorWidget:
    """
    Wrapper around Tkinter Text widget with additional functionality.
    """
    
    def __init__(self, parent, **kwargs):
        """
        Initialize editor widget.
        
        Args:
            parent: Parent widget
            **kwargs: Additional arguments for Text widget
        """
        self.parent = parent
        self.text = tk.Text(parent, wrap='word', undo=True, **kwargs)
        self.scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
    def pack(self, **kwargs):
        """Pack the editor widgets."""
        self.scrollbar.pack(side='right', fill='y')
        self.text.pack(side='left', fill='both', expand=True, **kwargs)
    
    def get_content(self):
        """Get all text content."""
        return self.text.get('1.0', tk.END)
    
    def set_content(self, content):
        """Set text content."""
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', content)
    
    def get_cursor_position(self):
        """Get current cursor position as (line, column)."""
        idx = self.text.index(tk.INSERT).split('.')
        return int(idx[0]), int(idx[1])
    
    def goto_line(self, line_number):
        """Move cursor to specified line number."""
        try:
            line_num = max(1, min(line_number, int(self.text.index('end-1c').split('.')[0])))
            self.text.mark_set(tk.INSERT, f'{line_num}.0')
            self.text.see(tk.INSERT)
        except Exception:
            pass


class MiniMap(tk.Canvas): ##
    def __init__(self, parent, text_widget, width=80):
        super().__init__(parent, width=width, highlightthickness=0)
        self.text = text_widget
        self.scale = 4  # lines per pixel

        self.bind("<Button-1>", self.on_click)

    def redraw(self):
        self.delete("all")

        height = self.winfo_height()
        width = self.winfo_width()
        if height <= 1:
            return

        # Blue bar ahh
        self.create_rectangle(0, 0, width, height, fill="#d0d0d0", outline="")

        # View
        first, last = self.text.yview()
        y1 = first * height
        y2 = last * height

        self.create_rectangle(
            0, y1, width, y2,
            fill="#8888ff", outline=""
        )


##showing the minimap
    def on_click(self, event):
        height = self.winfo_height()
        fraction = event.y / height
        self.text.yview_moveto(fraction)
