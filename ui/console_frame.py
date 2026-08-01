import tkinter as tk
from tkinter import scrolledtext
from ui.theme import *
from ui.widgets import neon_button
from core.i18n.translator import _

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
    def flush(self): pass

class ConsoleFrame(tk.Frame):
    def __init__(self, parent, on_back):
        super().__init__(parent, bg=BG_PANEL)
        
        header = tk.Frame(self, bg=BG_PANEL)
        header.pack(fill=tk.X, pady=(0, 8))
        tk.Label(header, text=_("bot_running"), bg=BG_PANEL, fg=CYAN, font=(FONT_MONO, 11, "bold")).pack(side=tk.LEFT)
        self.blink_label = tk.Label(header, text="●", bg=BG_PANEL, fg=NEON_GREEN, font=(FONT_MONO, 12))
        self.blink_label.pack(side=tk.LEFT, padx=8)
        self._blink_on = True
        self._blink_task = None

        border = tk.Frame(self, bg=CYAN, padx=1, pady=1)
        border.pack(fill=tk.BOTH, expand=True)

        self.text = scrolledtext.ScrolledText(
            border, wrap=tk.WORD, bg="#030710", fg=NEON_GREEN, font=(FONT_MONO, 8),
            insertbackground=CYAN, selectbackground=CYAN, selectforeground=BG_DEEP,
            borderwidth=0, relief="flat"
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.configure(state='disabled')

        self.btn_back_outer, self.btn_back_inner = neon_button(self, f"← {_('btn_back_menu')}", on_back, color=MAGENTA)
        self.btn_back_outer.pack(fill=tk.X, pady=(8, 0))

    def set_back_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.btn_back_inner.config(state=state)
        self.btn_back_outer.config(bg=MAGENTA if enabled else GRAY)

    def start_blink(self):
        self._blink_on = True
        self._blink()

    def _blink(self):
        self.blink_label.config(fg=NEON_GREEN if self._blink_on else BG_PANEL)
        self._blink_on = not self._blink_on
        self._blink_task = self.after(500, self._blink)

    def stop_blink(self):
        if self._blink_task:
            self.after_cancel(self._blink_task)
            self._blink_task = None
        self.blink_label.config(fg=BG_PANEL)
