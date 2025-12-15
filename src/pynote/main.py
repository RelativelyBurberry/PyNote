# src/pynote/main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "PyNote"

from utils import load_settings, save_settings #we need this for persistence
import time #

class PyNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings() #persistence
        self.title(APP_TITLE)
        self.geometry('800x600')
        self._filepath = None
        self._create_widgets()
        self._create_menu()
        self._bind_shortcuts()
        self._autosave_job = None #never ever miss these, it will break multiple times without this
        self._autosave_prompted = False #
        self._start_autosave() #

    def _create_widgets(self):
        # Text widget with scrollbar
        self.text = tk.Text(self, wrap='word', undo=True)
        self.vsb = ttk.Scrollbar(self, orient='vertical', command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side='right', fill='y')
        self.text.pack(side='left', fill='both', expand=True)

        # status bar
        self.status = tk.StringVar()
        self.status.set('Ln 1, Col 0')
        status_bar = ttk.Label(self, textvariable=self.status, anchor='w')
        status_bar.pack(side='bottom', fill='x')

        # update cursor position
        self.text.bind('<KeyRelease>', self._update_status)
        self.text.bind('<ButtonRelease>', self._update_status)

        self.text.bind('<Key>', lambda e: self.text.edit_modified(True)) # MARK TEXT AS MODIFIED FOR AUTOSAVE

    def _create_menu(self):
        menu = tk.Menu(self)
        filemenu = tk.Menu(menu, tearoff=0)
        filemenu.add_command(label='New', command=self.new_file)
        filemenu.add_command(label='Open', command=self.open_file)
        filemenu.add_command(label='Save', command=self.save_file)
        filemenu.add_command(label='Save As', command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quit)
        menu.add_cascade(label='File', menu=filemenu)
        self.config(menu=menu)

    def _bind_shortcuts(self):
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-z>', lambda e: self.text.event_generate('<<Undo>>'))
        self.bind('<Control-y>', lambda e: self.text.event_generate('<<Redo>>'))
        self.text.bind('<Key>', lambda e: self.text.edit_modified(True)) #check every key bind

    def new_file(self):
        if self._confirm_discard():
            self.text.delete('1.0', tk.END)
            self._filepath = None
            self.title(APP_TITLE)

    def open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            filetypes=[('Text Files', '*.txt;*.md;*.py'), ('All Files', '*.*')]
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                self.text.delete('1.0', tk.END)
                self.text.insert('1.0', data)
                self._filepath = path
                self.title(f"{APP_TITLE} - {path}")
            except Exception as e:
                messagebox.showerror('Error', f'Failed to open file: {str(e)}')

    def save_file(self):
        if self._filepath:
            try:
                with open(self._filepath, 'w', encoding='utf-8') as f:
                    f.write(self.text.get('1.0', tk.END))
                self.text.edit_modified(False)
                messagebox.showinfo('Saved', 'File saved successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save file: {str(e)}')
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text Files', '*.txt;*.md;*.py'), ('All Files', '*.*')]
        )
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.text.get('1.0', tk.END))
                self._filepath = path
                self.title(f"{APP_TITLE} - {path}")
                self.text.edit_modified(False)
                messagebox.showinfo('Saved', 'File saved successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save file: {str(e)}')

    #the main functions of the autosave -> Absolute Cinema 

    def _start_autosave(self):   ##the entry point -> starts the autosave
        interval_ms = 1000
        self._schedule_autosave(interval_ms)

    def _schedule_autosave(self, interval_ms): ##timer setup, cancel previous autosave state and make new
        if self._autosave_job:
            self.after_cancel(self._autosave_job)
        self._autosave_job = self.after(interval_ms, self._autosave)

    def _autosave(self):  ##the real GOAT -> check if any text has been modified, if not return, if yes, then call the silent save - ui nonblocking or propmt
        if not self.text.edit_modified():
            self._reschedule_autosave()
            return

        if self._filepath:
            self._silent_save()
        else:
            self._prompt_autosave_location() 

        self._reschedule_autosave() #and then reshedule it, runs once and then stops forever moment

    
    def _reschedule_autosave(self): #but then this guy keeps the loop alive, automatic self scheduling no params needed
        interval_ms = 1000
        self._autosave_job = self.after(interval_ms, self._autosave) 

    def _silent_save(self): #non block
        try:
            with open(self._filepath, 'w', encoding='utf-8') as f:
                f.write(self.text.get('1.0', tk.END))
            self.text.edit_modified(False)  ##**reset modified , dirty variable 😏
            self._show_autosave_indicator() 
        except Exception:
            pass    

    def _prompt_autosave_location(self): #the prompt if file hasnt been saved
        if self._autosave_prompted:
            return

        self._autosave_prompted = True
        resp = messagebox.askyesno(
            'Enable Autosave',
            'This file is not saved yet.\nDo you want to choose a location for autosave?'
        )
        if resp:
            self.save_as()

    def _show_autosave_indicator(self): #using the time module
        timestamp = time.strftime('%H:%M:%S')
        self.status.set(f'Autosaved at {timestamp}')

    ##end of Absolute Cinema

    def _update_status(self, event=None):
        idx = self.text.index(tk.INSERT).split('.')
        line = idx[0]
        col = idx[1]
        self.status.set(f'Ln {line}, Col {col}')

    def _confirm_discard(self):
        if self.text.edit_modified():
            resp = messagebox.askyesnocancel(
                'Unsaved changes',
                'You have unsaved changes. Save before continuing?'
            )
            if resp is None:
                return False
            if resp:
                self.save_file()
        return True


if __name__ == '__main__':
    app = PyNoteApp()
    app.mainloop()

