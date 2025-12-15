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


def show_about(parent):
    """Show about dialog."""
    AboutDialog(parent)

class PreferencesDialog: #Preferences DIalog box to choose width
    def __init__(self, parent, settings, on_apply):
        self.parent = parent
        self.settings = settings
        self.on_apply = on_apply

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Preferences")
        self.dialog.geometry("260x160")
        self.dialog.resizable(False, False)

        self.tab_size = tk.IntVar(value=settings.get('tab_size', 4))

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.dialog, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Tab width (spaces):").pack(anchor="w")

        for size in (2, 4, 8):
            tk.Radiobutton(
                frame,
                text=str(size),
                variable=self.tab_size,
                value=size
            ).pack(anchor="w")

        tk.Button(
            frame,
            text="Apply",
            width=10,
            command=self._apply
        ).pack(pady=10)

    def _apply(self):
        self.settings['tab_size'] = self.tab_size.get()
        self.on_apply(self.tab_size.get())
        self.dialog.destroy()

def show_preferences(parent, settings, on_apply): ## to apply the preferences
    PreferencesDialog(parent, settings, on_apply)
