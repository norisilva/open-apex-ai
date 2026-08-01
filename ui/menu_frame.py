import tkinter as tk
from ui.theme import *
from ui.widgets import neon_button

class MenuFrame(tk.Frame):
    def __init__(self, parent, on_scrape, on_config, on_hud, on_auto_config):
        super().__init__(parent, bg=BG_PANEL)
        
        header = tk.Frame(self, bg=BG_PANEL)
        header.pack(fill=tk.X, pady=(0, 12))
        tk.Label(header, text="F1  SETUPS  ASSIST", bg=BG_PANEL, fg=CYAN, font=(FONT_MONO, 17, "bold")).pack()
        tk.Label(header, text="◄ UNIVERSAL SETUP SYSTEM ►", bg=BG_PANEL, fg=MAGENTA, font=(FONT_MONO, 8)).pack()
        tk.Frame(self, bg=CYAN, height=1).pack(fill=tk.X, pady=(4, 16))

        self.status_var = tk.StringVar(value="SISTEMA PRONTO")
        status_chip = tk.Frame(self, bg=BG_CARD, padx=10, pady=6)
        status_chip.pack(fill=tk.X, pady=(0, 16))
        tk.Label(status_chip, text="●", bg=BG_CARD, fg=NEON_GREEN, font=(FONT_MONO, 10)).pack(side=tk.LEFT, padx=(0, 6))
        self.status_label = tk.Label(status_chip, textvariable=self.status_var, bg=BG_CARD, fg=NEON_GREEN, font=(FONT_MONO, 9))
        self.status_label.pack(side=tk.LEFT)

        btn_scrape, _ = neon_button(self, "[ 01 ]  BAIXAR SETUPS DA NUVEM", on_scrape, color=CYAN)
        btn_scrape.pack(fill=tk.X, pady=4)

        btn_cfg, _ = neon_button(self, "[ 02 ]  CONFIGURAR PERFIS", on_config, color=MAGENTA)
        btn_cfg.pack(fill=tk.X, pady=4)

        btn_hud, _ = neon_button(self, "[ 03 ]  INICIAR CENTRAL HUD INTELIGENTE", on_hud, color=NEON_GREEN)
        btn_hud.pack(fill=tk.X, pady=4)

        btn_auto_config, _ = neon_button(self, "[ 04 ]  AUTO-CONFIGURAR JOGO (TELEMETRIA)", on_auto_config, color=CYAN)
        btn_auto_config.pack(fill=tk.X, pady=4)

        tk.Frame(self, bg=GRAY, height=1).pack(fill=tk.X, pady=(16, 8))
        tk.Label(self, text="! Ao rodar o HUD, feche o F1Laps App", bg=BG_PANEL, fg=GRAY, font=(FONT_MONO, 7)).pack(anchor="w")

    def set_status(self, text, color=NEON_GREEN):
        self.status_var.set(text)
        self.status_label.config(fg=color)
