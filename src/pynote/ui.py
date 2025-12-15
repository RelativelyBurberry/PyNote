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

class FindReplaceDialog:
    def __init__(self, parent, text_widget):
        self.parent = parent
        self.text_widget = text_widget

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Find and Replace")
        self.dialog.geometry("400x220")
        self.dialog.resizable(False, False)

        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        self.case_sensitive = tk.BooleanVar()
        self.use_regex = tk.BooleanVar()

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.dialog, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Find
        tk.Label(frame, text="Find:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.find_var, width=30).grid(
            row=0, column=1, columnspan=2, pady=5
        )

        # Replace
        tk.Label(frame, text="Replace:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.replace_var, width=30).grid(
            row=1, column=1, columnspan=2, pady=5
        )

        # Options
        tk.Checkbutton(
            frame, text="Case Sensitive", variable=self.case_sensitive
        ).grid(row=2, column=1, sticky="w")

        tk.Checkbutton(
            frame, text="Regex", variable=self.use_regex
        ).grid(row=2, column=2, sticky="w")

        # Buttons
        tk.Button(frame, text="Replace", command=self.replace_one).grid(
            row=3, column=1, pady=15
        )

        tk.Button(frame, text="Replace All", command=self.replace_all).grid(
            row=3, column=2, pady=15
        )

    
    #Logiks
    def replace_one(self):
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()

        if not find_text:
            return

        content = self.text_widget.get("1.0", tk.END)

        flags = 0 if self.case_sensitive.get() else re.IGNORECASE

        try:
            if self.use_regex.get():
                new_content, count = re.subn(
                    find_text, replace_text, content, count=1, flags=flags
                )
            else:
                if not self.case_sensitive.get():
                    index = content.lower().find(find_text.lower())
                else:
                    index = content.find(find_text)

                if index == -1:
                    return

                new_content = (
                    content[:index]
                    + replace_text
                    + content[index + len(find_text):]
                )
                count = 1

            if count > 0:
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", new_content)

        except re.error as e:
            messagebox.showerror("Regex Error", str(e))

    def replace_all(self):
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()

        if not find_text:
            return

        content = self.text_widget.get("1.0", tk.END)

        flags = 0 if self.case_sensitive.get() else re.IGNORECASE

        try:
            if self.use_regex.get():
                new_content, count = re.subn(
                    find_text, replace_text, content, flags=flags
                )
            else:
                if self.case_sensitive.get():
                    count = content.count(find_text)
                    new_content = content.replace(find_text, replace_text)
                else:
                    pattern = re.compile(re.escape(find_text), re.IGNORECASE)
                    new_content, count = pattern.subn(replace_text, content)

            if count > 0:
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", new_content)
                messagebox.showinfo(
                    "Replace All",
                    f"Replaced {count} occurrence(s)."
                )

        except re.error as e:
            messagebox.showerror("Regex Error", str(e))
            
def show_about(parent):
    """Show about dialog."""
    AboutDialog(parent)

