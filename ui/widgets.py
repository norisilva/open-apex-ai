import tkinter as tk
from ui.theme import *

def neon_button(parent, text, cmd, color=CYAN, width=None):
    outer = tk.Frame(parent, bg=color, padx=1, pady=1)
    btn = tk.Button(
        outer, text=text, command=cmd, bg=BG_CARD, fg=color,
        font=(FONT_MONO, 10, "bold"), activebackground=color,
        activeforeground=BG_DEEP, relief="flat", cursor="hand2",
        padx=16, pady=10, bd=0
    )
    btn.pack(fill=tk.BOTH, expand=True)

    def on_enter(e): btn.config(bg=color, fg=BG_DEEP)
    def on_leave(e): btn.config(bg=BG_CARD, fg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    if width:
        outer.config(width=width)
    return outer, btn

def cyber_label(parent, text, color=WHITE, size=10, bold=False):
    font_weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, bg=BG_PANEL, fg=color, font=(FONT_MONO, size, font_weight))

class CyberTitleBar(tk.Frame):
    def __init__(self, parent, title, on_close, on_minimize, **kwargs):
        super().__init__(parent, bg=BG_DEEP, height=36, **kwargs)
        self.pack_propagate(False)

        tk.Frame(self, bg=CYAN, height=2).pack(fill=tk.X, side=tk.TOP)
        content = tk.Frame(self, bg=BG_DEEP)
        content.pack(fill=tk.BOTH, expand=True)

        tk.Label(content, text="◈", bg=BG_DEEP, fg=CYAN, font=(FONT_MONO, 11, "bold")).pack(side=tk.LEFT, padx=(10, 4))
        tk.Label(content, text=title, bg=BG_DEEP, fg=WHITE, font=(FONT_MONO, 9)).pack(side=tk.LEFT)

        btn_close = tk.Label(content, text="✕", bg=BG_DEEP, fg=GRAY, font=(FONT_MONO, 11), cursor="hand2", padx=10)
        btn_close.pack(side=tk.RIGHT)
        btn_close.bind("<Enter>", lambda e: btn_close.config(fg=MAGENTA))
        btn_close.bind("<Leave>", lambda e: btn_close.config(fg=GRAY))
        btn_close.bind("<Button-1>", lambda e: on_close())

        btn_min = tk.Label(content, text="─", bg=BG_DEEP, fg=GRAY, font=(FONT_MONO, 11), cursor="hand2", padx=10)
        btn_min.pack(side=tk.RIGHT)
        btn_min.bind("<Enter>", lambda e: btn_min.config(fg=CYAN))
        btn_min.bind("<Leave>", lambda e: btn_min.config(fg=GRAY))
        btn_min.bind("<Button-1>", lambda e: on_minimize())

        self._x = self._y = 0
        for w in [self, content]:
            w.bind("<ButtonPress-1>", self._start_drag)
            w.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        self._x = event.x_root - self.winfo_toplevel().winfo_x()
        self._y = event.y_root - self.winfo_toplevel().winfo_y()

    def _do_drag(self, event):
        x = event.x_root - self._x
        y = event.y_root - self._y
        self.winfo_toplevel().geometry(f"+{x}+{y}")
