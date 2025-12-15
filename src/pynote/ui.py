# src/pynote/ui.py
"""
UI components (menus, dialogs) for PyNote.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog


class AboutDialog:
    """About dialog for PyNote."""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title('About PyNote')
        self.dialog.geometry('300x200')
        self.dialog.resizable(False, False)
        self._create_widgets()
    
    def _create_widgets(self):
        tk.Label(
            self.dialog,
            text='PyNote',
            font=('Arial', 16, 'bold')
        ).pack(pady=10)
        
        tk.Label(
            self.dialog,
            text='A Beginner-Friendly Desktop Text Editor',
            font=('Arial', 10)
        ).pack(pady=5)
        
        tk.Label(
            self.dialog,
            text='Version 0.1.0',
            font=('Arial', 9)
        ).pack(pady=5)
        
        tk.Label(
            self.dialog,
            text='Built with Python + Tkinter',
            font=('Arial', 8)
        ).pack(pady=5)
        
        tk.Button(
            self.dialog,
            text='OK',
            command=self.dialog.destroy,
            width=10
        ).pack(pady=20)


class GoToLineDialog:
    """Go to line number dialog."""
    
    def __init__(self, parent, max_lines):
        self.parent = parent
        self.max_lines = max_lines
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title('Go to Line')
        self.dialog.geometry('250x100')
        self.dialog.resizable(False, False)
        self._create_widgets()
    
    def _create_widgets(self):
        tk.Label(
            self.dialog,
            text=f'Enter line number (1-{self.max_lines}):'
        ).pack(pady=10)
        
        self.entry = tk.Entry(self.dialog, width=20)
        self.entry.pack(pady=5)
        self.entry.focus()
        self.entry.bind('<Return>', lambda e: self._ok())
        
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text='OK',
            command=self._ok,
            width=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text='Cancel',
            command=self.dialog.destroy,
            width=8
        ).pack(side='left', padx=5)
    
    def _ok(self):
        try:
            line_num = int(self.entry.get())
            if 1 <= line_num <= self.max_lines:
                self.result = line_num
                self.dialog.destroy()
            else:
                messagebox.showerror(
                    'Error',
                    f'Line number must be between 1 and {self.max_lines}'
                )
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid number')

class FindDialog: #Find Dialog Box Moment

    def __init__(self, parent, text_widget,on_close=None): #added on-close for only 1 dialog box of find
        self.on_close = on_close #
        self.parent = parent
        self.text = text_widget
        self.last_index = "1.0"

        self.dialog = tk.Toplevel(parent)
        self.dialog.protocol("WM_DELETE_WINDOW", self._close) # handle close event 
        self.dialog.title("Find")
        self.dialog.geometry("320x160")
        self.dialog.resizable(False, False)

        self.find_var = tk.StringVar()
        self.case_sensitive = tk.BooleanVar()

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.dialog, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Find:").grid(row=0, column=0, sticky="w")
        entry = tk.Entry(frame, textvariable=self.find_var, width=28)
        entry.grid(row=0, column=1, columnspan=2, pady=5)
        entry.focus()

        tk.Checkbutton(
            frame, text="Case sensitive", variable=self.case_sensitive
        ).grid(row=1, column=1, sticky="w")

        tk.Button(frame, text="Next", width=8, command=self.find_next).grid(
            row=2, column=1, pady=10
        )
        tk.Button(frame, text="Previous", width=8, command=self.find_prev).grid(
            row=2, column=2, pady=10
        )

    #find logiks moment

    def _search(self, backwards=False):
        term = self.find_var.get()
        if not term:
            return

        self.text.tag_remove("find_highlight", "1.0", tk.END)

        flags = {}
        if not self.case_sensitive.get():
            flags["nocase"] = True

        start = self.last_index
        if backwards:
            start = self.text.index(f"{start} -1c")

        pos = self.text.search(
            term,
            start,
            stopindex=tk.END if not backwards else "1.0",
            backwards=backwards,
            **flags
        )

        if not pos:
            self.last_index = "1.0"
            return

        end = f"{pos}+{len(term)}c"
        self.text.tag_add("find_highlight", pos, end)
        self.text.tag_config("find_highlight", background="yellow")

        self.text.mark_set(tk.INSERT, end)
        self.text.see(pos)

        self.last_index = end

    def find_next(self):
        self._search(backwards=False)

    def find_prev(self):
        self._search(backwards=True)

def show_find_dialog(parent, text_widget): ## to call the find 
    FindDialog(parent, text_widget)
    
def show_about(parent):
    """Show about dialog."""
    AboutDialog(parent)

