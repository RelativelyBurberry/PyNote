# src/pynote/main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "PyNote"

import re ##

#list of keywords
PYTHON_KEYWORDS = { 
    "False","None","True","and","as","assert","async","await","break",
    "class","continue","def","del","elif","else","except","finally",
    "for","from","global","if","import","in","is","lambda","nonlocal",
    "not","or","pass","raise","return","try","while","with","yield"
}

JS_KEYWORDS = {
    "break","case","catch","class","const","continue","debugger","default",
    "delete","do","else","export","extends","finally","for","function",
    "if","import","in","instanceof","let","new","return","super",
    "switch","this","throw","try","typeof","var","void","while","yield"
}

def _configure_syntax_tags(self): ##color mapping
        self.text.tag_config("keyword", foreground="#569CD6")   # blue
        self.text.tag_config("string", foreground="#CE9178")    # orange
        self.text.tag_config("comment", foreground="#6A9955")   # green

class PyNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
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
        status_bar = ttk.Label(self, textvariable=self.status, anchor='w')
        status_bar.pack(side='bottom', fill='x')

        # update cursor position
        self.text.bind('<KeyRelease>', self._update_status)
        self.text.bind('<ButtonRelease>', self._update_status)

        self._configure_syntax_tags() ## 
        self.text.bind("<KeyRelease>", lambda e: self._highlight_syntax()) ## 


    ##functions
    def _detect_language(self): ##detecting the language 
        if not self._filepath:
            return None
        if self._filepath.endswith(".py"):
            return "python"
        if self._filepath.endswith(".js"):
            return "javascript"
        return None
    
    def _highlight_syntax(self): ##
        language = self._detect_language()
        print("LANG =", language)   # 


        text = self.text.get("1.0", tk.END)
    
        # Clear old tags
        for tag in ("keyword", "string", "comment"):
            self.text.tag_remove(tag, "1.0", tk.END)

        if language == "python":
            keywords = PYTHON_KEYWORDS
            comment_pattern = r"#.*"
            string_pattern = r"(\".*?\"|\'.*?\')"
        else:  #  javascript  
            keywords = JS_KEYWORDS
            comment_pattern = r"//.*"
            string_pattern = r"(\".*?\"|\'.*?\'|\`.*?\`)"

        # Highlight  comments
        for match in re.finditer(comment_pattern, text):
            self._apply_tag(match, "comment")

        # Strings
        for match in re.finditer(string_pattern, text):
            self._apply_tag(match, "string")

        # Keywowrds
        for word in keywords:
            pattern = r"\b" + re.escape(word) + r"\b"
            for match in re.finditer(pattern, text):
                self._apply_tag(match, "keyword")

    def _apply_tag(self, match, tag): ###
        start = match.start()
        end = match.end()

        start_index = f"1.0+{start}c"
        end_index = f"1.0+{end}c"

        self.text.tag_add(tag, start_index, end_index)

    #end of functions

    
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

    def new_file(self):
        if self._confirm_discard():
            self.text.delete('1.0', tk.END)
            self._filepath = None
            self.title(APP_TITLE)

    def open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            filetypes=[('Text Files', '*.txt;*.md;*.py;*.js'), ('All Files', '*.*')] #Adding js filetype as well
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                self.text.delete('1.0', tk.END)
                self.text.insert('1.0', data)
                self._filepath = path
                self.title(f"{APP_TITLE} - {path}")
                self._highlight_syntax() ##
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
            filetypes=[('Text Files', '*.txt;*.md;*.py;*.js'), ('All Files',  '*.*')] #here also js
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

