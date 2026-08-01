import tkinter as tk
from ui.theme import *

class EdgeTrigger(tk.Toplevel):
    def __init__(self, on_click):
        super().__init__()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.7)
        
        # Posicionar no meio do lado esquerdo da tela
        screen_height = self.winfo_screenheight()
        y_pos = (screen_height // 2) - 50
        self.geometry(f"30x100+0+{y_pos}")
        self.configure(bg=CYAN) # Borda direita
        
        # Efeito de hover
        self.bind("<Enter>", lambda e: self.attributes("-alpha", 1.0))
        self.bind("<Leave>", lambda e: self.attributes("-alpha", 0.7))
        
        frame = tk.Frame(self, bg=BG_DEEP, padx=2, pady=2)
        # Deixar a borda direita maior para dar efeito
        frame.pack(fill=tk.BOTH, expand=True, padx=(0, 2), pady=2)
        
        lbl = tk.Label(frame, text="▶", bg=BG_DEEP, fg=CYAN, font=(FONT_MONO, 12))
        lbl.pack(expand=True)
        
        # Bind de cliques para restaurar janela
        self.bind("<ButtonRelease-1>", lambda e: on_click())
        frame.bind("<ButtonRelease-1>", lambda e: on_click())
        lbl.bind("<ButtonRelease-1>", lambda e: on_click())
