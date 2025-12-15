# src/pynote/ui.py
"""
UI components (menus, dialogs) for PyNote.
"""
import sys #added this for the cross-platform thingie

import tkinter as tk
from tkinter import messagebox, simpledialog

def shortcut_key(): ##cross platform retrn value
    return "Cmd" if sys.platform == "darwin" else "Ctrl"

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

class ShortcutGuideDialog: ### Dialog Box of Shortcuts

    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Keyboard Shortcuts")
        self.dialog.geometry("420x320")
        self.dialog.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):
        key = shortcut_key()

        container = tk.Frame(self.dialog, padx=15, pady=10)
        container.pack(fill="both", expand=True)

        def section(title):
            tk.Label(
                container,
                text=title,
                font=("Arial", 11, "bold")
            ).pack(anchor="w", pady=(10, 4))

        def item(name, combo):
            tk.Label(
                container,
                text=f"{name:<20} {combo}",
                font=("Courier New", 10)
            ).pack(anchor="w")

        # File Shortcuts
        section("File")
        item("New File", f"{key}+N")
        item("Open File", f"{key}+O")
        item("Save", f"{key}+S")
        item("Save As", f"{key}+Shift+S")

        # Editing Shortcuts
        section("Edit")
        item("Undo", f"{key}+Z")
        item("Redo", f"{key}+Y")
        item("Find", f"{key}+F")

        # View Shortcuts
        section("View")
        item("Toggle Status Bar", f"{key}+B")

        tk.Button(
            container,
            text="Close",
            width=10,
            command=self.dialog.destroy
        ).pack(pady=15)

def show_shortcuts(parent): #to show the dialog box
    ShortcutGuideDialog(parent)


def show_about(parent):
    """Show about dialog."""
    AboutDialog(parent)

