# src/pynote/main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "PyNote"

from utils import load_settings, save_settings #we need those thingies chat
#i wrote all the comments myself its not AI

class PyNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()

        #Sub Issue 2 -> Persistent across all sessions
        #This saves the visibility of status bar, so when pynote restarts it remembers if it was on or off
        self.settings = load_settings() #
        self.show_status_bar = tk.BooleanVar( #
            value=self.settings.get('show_status_bar', True) #
        )

        
        self.title(APP_TITLE)
        self.geometry('800x600')
        self._filepath = None
        self._create_widgets()
        self._create_menu()
        self._bind_shortcuts()

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
        self.status_bar = ttk.Label(self, textvariable=self.status, anchor='w')  # Added self to both of these to make it a part of the object
        self.status_bar.pack(side='bottom', fill='x') #


        # Apply the saved states
        if not self.show_status_bar.get(): #
            self.status_bar.pack_forget() #
            
        # update cursor position
        self.text.bind('<KeyRelease>', self._update_status)
        self.text.bind('<ButtonRelease>', self._update_status)

    #toggle function
    def toggle_status_bar(self):
        if self.show_status_bar.get():
            self.status_bar.pack(side='bottom', fill='x')
        else:
            self.status_bar.pack_forget()

        # Persist setting
        self.settings['show_status_bar'] = self.show_status_bar.get()
        save_settings(self.settings)

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
        viewmenu = tk.Menu(menu, tearoff=0) ## Sub-Issue 3 -> Menu
        viewmenu.add_checkbutton( #
            label="Status Bar", #
            variable=self.show_status_bar,
            command=self.toggle_status_bar
        )
        menu.add_cascade(label="View", menu=viewmenu)
        self.config(menu=menu)

    def _bind_shortcuts(self):
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<Control-o>', lambda e: self.open_file())
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-z>', lambda e: self.text.event_generate('<<Undo>>'))
        self.bind('<Control-y>', lambda e: self.text.event_generate('<<Redo>>'))
        self.bind('<Control-b>', lambda e: self._toggle_status_shortcut()) # Sub Issue 1 ->Binding key to Ctrl B

    #and the definition for that shortcut
    def _toggle_status_shortcut(self): # 
        self.show_status_bar.set(not self.show_status_bar.get()) 
        self.toggle_status_bar() 

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

