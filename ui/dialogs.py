import tkinter as tk
from ui.theme import *
from ui.widgets import neon_button

class CyberDialog(tk.Toplevel):
    def __init__(self, parent, title, message, error=False):
        super().__init__(parent)
        self.overrideredirect(True)
        color = MAGENTA if error else CYAN
        self.configure(bg=color)
        self.transient(parent)

        px = max(0, parent.winfo_x() + (parent.winfo_width() // 2) - 180)
        py = max(0, parent.winfo_y() + (parent.winfo_height() // 2) - 90)
        self.geometry(f"360x180+{px}+{py}")
        
        self.update_idletasks()
        self.attributes('-topmost', True)
        self.grab_set()

        inner = tk.Frame(self, bg=BG_PANEL, padx=20, pady=16)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        tk.Label(inner, text=f"◈ {title}", bg=BG_PANEL, fg=color, font=(FONT_MONO, 11, "bold")).pack(anchor="w")
        tk.Frame(inner, bg=color, height=1).pack(fill=tk.X, pady=8)
        tk.Label(inner, text=message, bg=BG_PANEL, fg=WHITE, font=(FONT_MONO, 9), wraplength=300, justify="left").pack(anchor="w")

        btn_ok, _ = neon_button(inner, "[ OK ]", self.destroy, color=color)
        btn_ok.pack(pady=(12, 0))
