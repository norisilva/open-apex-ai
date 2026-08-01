import sys
import tkinter as tk
from tkinter import scrolledtext
import threading
import json
import os

import config
from scraper.dual_scraper import DualScraper
from transformer.accessibility_engine import AccessibilityTransformer

# ─── PALETA CYBERPUNK ────────────────────────────────────────────────────────
BG_DEEP    = "#080c14"
BG_PANEL   = "#0d1117"
BG_CARD    = "#111827"
CYAN       = "#00f5ff"
MAGENTA    = "#ff00aa"
NEON_GREEN = "#39ff14"
NEON_YELLOW= "#f5e642"
WHITE      = "#e2e8f0"
GRAY       = "#4a5568"
FONT_MONO  = "Consolas"
FONT_MAIN  = "Segoe UI"


def neon_button(parent, text, cmd, color=CYAN, width=None):
    """Botao flat estilo cyberpunk com borda neon e hover."""
    outer = tk.Frame(parent, bg=color, padx=1, pady=1)
    btn = tk.Button(
        outer,
        text=text,
        command=cmd,
        bg=BG_CARD,
        fg=color,
        font=(FONT_MONO, 10, "bold"),
        activebackground=color,
        activeforeground=BG_DEEP,
        relief="flat",
        cursor="hand2",
        padx=16,
        pady=10,
        bd=0,
    )
    btn.pack(fill=tk.BOTH, expand=True)

    def on_enter(e):
        btn.config(bg=color, fg=BG_DEEP)
    def on_leave(e):
        btn.config(bg=BG_CARD, fg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    if width:
        outer.config(width=width)
    return outer, btn


def cyber_label(parent, text, color=WHITE, size=10, bold=False):
    font_weight = "bold" if bold else "normal"
    return tk.Label(
        parent,
        text=text,
        bg=BG_PANEL,
        fg=color,
        font=(FONT_MONO, size, font_weight),
    )


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass


class CyberTitleBar(tk.Frame):
    """Barra de titulo customizada sem a barra nativa do Windows."""

    def __init__(self, parent, title, on_close, on_minimize, **kwargs):
        super().__init__(parent, bg=BG_DEEP, height=36, **kwargs)
        self.pack_propagate(False)

        # Linha neon no topo
        accent_line = tk.Frame(self, bg=CYAN, height=2)
        accent_line.pack(fill=tk.X, side=tk.TOP)

        # Conteudo da barra
        content = tk.Frame(self, bg=BG_DEEP)
        content.pack(fill=tk.BOTH, expand=True)

        # Icone + Titulo
        tk.Label(content, text="◈", bg=BG_DEEP, fg=CYAN, font=(FONT_MONO, 11, "bold")).pack(side=tk.LEFT, padx=(10, 4))
        tk.Label(content, text=title, bg=BG_DEEP, fg=WHITE, font=(FONT_MONO, 9)).pack(side=tk.LEFT)

        # Botoes de controle
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

        # Dragging
        self._x = 0
        self._y = 0
        self.bind("<ButtonPress-1>", self._start_drag)
        self.bind("<B1-Motion>", self._do_drag)
        content.bind("<ButtonPress-1>", self._start_drag)
        content.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        self._x = event.x_root - self.winfo_toplevel().winfo_x()
        self._y = event.y_root - self.winfo_toplevel().winfo_y()

    def _do_drag(self, event):
        x = event.x_root - self._x
        y = event.y_root - self._y
        self.winfo_toplevel().geometry(f"+{x}+{y}")


class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()

        # ── Janela sem barra nativa ──────────────────────────────────────────
        self.overrideredirect(True)           # remove barra de titulo nativa
        self.geometry("420x520+100+80")
        self.configure(bg=BG_DEEP)
        self.wm_attributes("-topmost", False)

        # Borda neon externa (frame wrapper com cor de borda)
        outer = tk.Frame(self, bg=CYAN, padx=1, pady=1)
        outer.pack(fill=tk.BOTH, expand=True)

        inner = tk.Frame(outer, bg=BG_DEEP, padx=1, pady=1)
        inner.pack(fill=tk.BOTH, expand=True)

        # ── Barra de titulo customizada ──────────────────────────────────────
        self.title_bar = CyberTitleBar(
            inner,
            title="F1 SETUPS ASSIST  //  v2.0",
            on_close=self.destroy,
            on_minimize=self.iconify,
        )
        self.title_bar.pack(fill=tk.X)

        # ── Painel Principal ─────────────────────────────────────────────────
        self.main_panel = tk.Frame(inner, bg=BG_PANEL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        # Container para telas (navegacao)
        self.container = tk.Frame(self.main_panel, bg=BG_PANEL)
        self.container.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        # ── Tela 1: MENU ─────────────────────────────────────────────────────
        self.menu_frame = tk.Frame(self.container, bg=BG_PANEL)

        # Logo / Header area
        header = tk.Frame(self.menu_frame, bg=BG_PANEL)
        header.pack(fill=tk.X, pady=(0, 12))

        tk.Label(
            header,
            text="F1  SETUPS  ASSIST",
            bg=BG_PANEL,
            fg=CYAN,
            font=(FONT_MONO, 17, "bold"),
        ).pack()

        tk.Label(
            header,
            text="◄ UNIVERSAL SETUP SYSTEM ►",
            bg=BG_PANEL,
            fg=MAGENTA,
            font=(FONT_MONO, 8),
        ).pack()

        # Linha separadora
        tk.Frame(self.menu_frame, bg=CYAN, height=1).pack(fill=tk.X, pady=(4, 16))

        # Status chip
        self.status_var = tk.StringVar(value="SISTEMA PRONTO")
        status_chip = tk.Frame(self.menu_frame, bg=BG_CARD, padx=10, pady=6)
        status_chip.pack(fill=tk.X, pady=(0, 16))
        tk.Label(status_chip, text="●", bg=BG_CARD, fg=NEON_GREEN, font=(FONT_MONO, 10)).pack(side=tk.LEFT, padx=(0, 6))
        self.status_label = tk.Label(status_chip, textvariable=self.status_var, bg=BG_CARD, fg=NEON_GREEN, font=(FONT_MONO, 9))
        self.status_label.pack(side=tk.LEFT)

        # Botoes
        self.btn_scrape_outer, self.btn_scrape = neon_button(
            self.menu_frame, "[ 01 ]  BAIXAR SETUPS DA NUVEM", self.run_scraper, color=CYAN
        )
        self.btn_scrape_outer.pack(fill=tk.X, pady=4)

        btn_cfg_outer, _ = neon_button(
            self.menu_frame, "[ 02 ]  CONFIGURAR PERFIS", self.open_settings, color=MAGENTA
        )
        btn_cfg_outer.pack(fill=tk.X, pady=4)

        btn_hud_outer, _ = neon_button(
            self.menu_frame, "[ 03 ]  INICIAR HUD NO JOGO", self.run_overlay, color=NEON_GREEN
        )
        btn_hud_outer.pack(fill=tk.X, pady=4)

        # Footer
        tk.Frame(self.menu_frame, bg=GRAY, height=1).pack(fill=tk.X, pady=(16, 8))
        tk.Label(
            self.menu_frame,
            text="! Ao rodar o HUD, feche o F1Laps App",
            bg=BG_PANEL,
            fg=GRAY,
            font=(FONT_MONO, 7),
        ).pack(anchor="w")

        # ── Tela 2: CONSOLE ──────────────────────────────────────────────────
        self.console_frame = tk.Frame(self.container, bg=BG_PANEL)

        # Header do console
        console_header = tk.Frame(self.console_frame, bg=BG_PANEL)
        console_header.pack(fill=tk.X, pady=(0, 8))
        tk.Label(console_header, text="◈ ROBO EM EXECUCAO", bg=BG_PANEL, fg=CYAN, font=(FONT_MONO, 11, "bold")).pack(side=tk.LEFT)

        # Blink indicator
        self.blink_label = tk.Label(console_header, text="●", bg=BG_PANEL, fg=NEON_GREEN, font=(FONT_MONO, 12))
        self.blink_label.pack(side=tk.LEFT, padx=8)
        self._blink_on = True
        self._blink_task = None

        # Console text area com borda neon
        console_border = tk.Frame(self.console_frame, bg=CYAN, padx=1, pady=1)
        console_border.pack(fill=tk.BOTH, expand=True)

        self.console_text = scrolledtext.ScrolledText(
            console_border,
            wrap=tk.WORD,
            bg="#030710",
            fg=NEON_GREEN,
            font=(FONT_MONO, 8),
            insertbackground=CYAN,
            selectbackground=CYAN,
            selectforeground=BG_DEEP,
            borderwidth=0,
            relief="flat",
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
        self.console_text.configure(state='disabled')

        # Botao Voltar (desabilitado enquanto roda)
        btn_back_outer, self.btn_back_inner = neon_button(
            self.console_frame, "← VOLTAR AO MENU", self.show_menu, color=MAGENTA
        )
        btn_back_outer.pack(fill=tk.X, pady=(8, 0))
        self.btn_back_outer = btn_back_outer

        self.show_menu()

    # ── NAVEGACAO ─────────────────────────────────────────────────────────────
    def show_menu(self):
        self._stop_blink()
        self.console_frame.pack_forget()
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

    def show_console(self):
        self.menu_frame.pack_forget()
        self.console_frame.pack(fill=tk.BOTH, expand=True)
        self._start_blink()

    # ── BLINK INDICATOR ──────────────────────────────────────────────────────
    def _start_blink(self):
        self._blink_on = True
        self._blink()

    def _blink(self):
        if self._blink_on:
            self.blink_label.config(fg=NEON_GREEN)
        else:
            self.blink_label.config(fg=BG_PANEL)
        self._blink_on = not self._blink_on
        self._blink_task = self.after(500, self._blink)

    def _stop_blink(self):
        if self._blink_task:
            self.after_cancel(self._blink_task)
            self._blink_task = None
        self.blink_label.config(fg=BG_PANEL)

    # ── ACOES ─────────────────────────────────────────────────────────────────
    def run_scraper(self):
        self.show_console()
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')
        self._set_back_enabled(False)

        def scrape_thread():
            old_stdout = sys.stdout
            sys.stdout = ConsoleRedirector(self.console_text)
            try:
                print("╔══════════════════════════════════════╗")
                print("║  INICIANDO EXTRACAO DE SETUPS        ║")
                print("╚══════════════════════════════════════╝\n")
                scraper = DualScraper()
                scraper.run()
                print("\n[ OK ] Aplicando perfis matematicos...")
                transformer = AccessibilityTransformer()
                transformer.run()
                print("\n╔══════════════════════════════════════╗")
                print("║  CONCLUIDO COM SUCESSO!              ║")
                print("╚══════════════════════════════════════╝")
                self.status_var.set("SETUPS ATUALIZADOS!")
                self.status_label.config(fg=NEON_GREEN)
            except Exception as e:
                print(f"\n[ERRO] {e}")
                self.status_var.set("ERRO NA EXTRACAO")
                self.status_label.config(fg=MAGENTA)
            finally:
                sys.stdout = old_stdout
                self._set_back_enabled(True)
                self._stop_blink()

        threading.Thread(target=scrape_thread, daemon=True).start()

    def _set_back_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.btn_back_inner.config(state=state)
        if enabled:
            self.btn_back_outer.config(bg=MAGENTA)
        else:
            self.btn_back_outer.config(bg=GRAY)

    def open_settings(self):
        SettingsWindow(self)

    def run_overlay(self):
        try:
            from overlay.overlay_ui import OverlayApp
            self.iconify()
            app = OverlayApp()
            app.run()
            self.deiconify()
        except ImportError as e:
            CyberDialog(self, "ERRO", f"Erro ao iniciar o HUD:\n{e}", error=True)


class CyberDialog(tk.Toplevel):
    """Caixa de dialogo estilo cyberpunk."""
    def __init__(self, parent, title, message, error=False):
        super().__init__(parent)
        self.overrideredirect(True)
        color = MAGENTA if error else CYAN
        self.configure(bg=color)
        self.geometry("360x180")
        self.transient(parent)
        self.grab_set()

        # Centraliza relativo ao parent
        px = parent.winfo_x() + (parent.winfo_width() // 2) - 180
        py = parent.winfo_y() + (parent.winfo_height() // 2) - 90
        self.geometry(f"+{px}+{py}")

        inner = tk.Frame(self, bg=BG_PANEL, padx=20, pady=16)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        tk.Label(inner, text=f"◈ {title}", bg=BG_PANEL, fg=color, font=(FONT_MONO, 11, "bold")).pack(anchor="w")
        tk.Frame(inner, bg=color, height=1).pack(fill=tk.X, pady=8)
        tk.Label(inner, text=message, bg=BG_PANEL, fg=WHITE, font=(FONT_MONO, 9), wraplength=300, justify="left").pack(anchor="w")

        btn_ok_outer, _ = neon_button(inner, "[ OK ]", self.destroy, color=color)
        btn_ok_outer.pack(pady=(12, 0))


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg=MAGENTA)
        self.geometry("400x480")
        self.transient(parent)
        self.grab_set()

        px = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        py = parent.winfo_y() + (parent.winfo_height() // 2) - 240
        self.geometry(f"+{px}+{py}")

        inner = tk.Frame(self, bg=BG_PANEL)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Titulo customizado com drag
        title_bar = tk.Frame(inner, bg=BG_DEEP, height=36)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Frame(title_bar, bg=MAGENTA, height=2).pack(fill=tk.X, side=tk.TOP)
        title_content = tk.Frame(title_bar, bg=BG_DEEP)
        title_content.pack(fill=tk.BOTH, expand=True)
        tk.Label(title_content, text="◈ CONFIGURAR PERFIL", bg=BG_DEEP, fg=MAGENTA, font=(FONT_MONO, 9, "bold")).pack(side=tk.LEFT, padx=10)
        close_btn = tk.Label(title_content, text="✕", bg=BG_DEEP, fg=GRAY, font=(FONT_MONO, 11), cursor="hand2", padx=10)
        close_btn.pack(side=tk.RIGHT)
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=MAGENTA))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=GRAY))
        close_btn.bind("<Button-1>", lambda e: self.destroy())

        # Drag
        self._x = self._y = 0
        for w in [title_bar, title_content]:
            w.bind("<ButtonPress-1>", self._start_drag)
            w.bind("<B1-Motion>", self._do_drag)

        # Content
        content = tk.Frame(inner, bg=BG_PANEL, padx=20, pady=16)
        content.pack(fill=tk.BOTH, expand=True)

        # Carregar rules
        self.rules_data = {}
        if os.path.exists(config.RULES_FILE):
            try:
                with open(config.RULES_FILE, 'r') as f:
                    self.rules_data = json.load(f)
            except:
                pass

        self.current_mode = self.rules_data.get("mode", "Acessibilidade (Max Estabilidade)")
        susp_factor = self.rules_data.get("suspension", {}).get("front_suspension", {}).get("factor", 0.75)
        diff_max    = self.rules_data.get("transmission", {}).get("on_throttle", {}).get("clamp_max", 52)
        brake_offset= self.rules_data.get("brakes", {}).get("brake_pressure", {}).get("offset", -5)

        # Dropdown
        tk.Label(content, text="MODO DE CONDUCAO", bg=BG_PANEL, fg=MAGENTA, font=(FONT_MONO, 8, "bold")).pack(anchor="w", pady=(0, 4))
        self.mode_var = tk.StringVar(value=self.current_mode)
        self.modes = ["Esports (Original)", "Gamepad (Estavel)", "Acessibilidade (Max Estabilidade)", "Personalizado"]

        mode_frame = tk.Frame(content, bg=MAGENTA, padx=1, pady=1)
        mode_frame.pack(fill=tk.X, pady=(0, 14))
        self.mode_combo = tk.OptionMenu(mode_frame, self.mode_var, *self.modes, command=self._on_mode_change)
        self.mode_combo.config(
            bg=BG_CARD, fg=MAGENTA, font=(FONT_MONO, 9),
            activebackground=BG_CARD, activeforeground=MAGENTA,
            highlightthickness=0, bd=0, relief="flat", indicatoron=True,
        )
        self.mode_combo["menu"].config(bg=BG_CARD, fg=MAGENTA, font=(FONT_MONO, 9), activebackground=MAGENTA, activeforeground=BG_DEEP)
        self.mode_combo.pack(fill=tk.X)

        # Sliders
        self.susp_var  = tk.DoubleVar(value=susp_factor)
        self.diff_var  = tk.IntVar(value=diff_max)
        self.brake_var = tk.IntVar(value=brake_offset)

        self._make_slider(content, "RIGIDEZ DA SUSPENSAO",       self.susp_var,  0.5,  1.0)
        self._make_slider(content, "DIFERENCIAL MAX (ACELERADA)", self.diff_var,  50,   100)
        self._make_slider(content, "PRESSAO DO FREIO (OFFSET)",   self.brake_var, -15,  0)

        # Botoes
        tk.Frame(content, bg=GRAY, height=1).pack(fill=tk.X, pady=12)
        btn_row = tk.Frame(content, bg=BG_PANEL)
        btn_row.pack(fill=tk.X)

        btn_cancel, _ = neon_button(btn_row, "CANCELAR", self.destroy, color=GRAY)
        btn_cancel.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))

        btn_save, _ = neon_button(btn_row, "SALVAR ► APLICAR", self.save_and_apply, color=MAGENTA)
        btn_save.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))

    def _make_slider(self, parent, label, variable, from_, to_):
        tk.Label(parent, text=label, bg=BG_PANEL, fg=CYAN, font=(FONT_MONO, 7, "bold")).pack(anchor="w", pady=(8, 2))
        slider_frame = tk.Frame(parent, bg=BG_PANEL)
        slider_frame.pack(fill=tk.X)
        s = tk.Scale(
            slider_frame,
            variable=variable,
            from_=from_, to=to_,
            orient=tk.HORIZONTAL,
            bg=BG_CARD, fg=CYAN,
            troughcolor=BG_DEEP,
            activebackground=CYAN,
            highlightthickness=0, bd=0,
            sliderlength=18, showvalue=True,
            font=(FONT_MONO, 7),
        )
        s.pack(fill=tk.X)
        s.bind("<ButtonRelease-1>", lambda e: self.mode_var.set("Personalizado"))

    def _on_mode_change(self, mode):
        if mode == "Esports (Original)":
            self.susp_var.set(1.0); self.diff_var.set(100); self.brake_var.set(0)
        elif mode == "Gamepad (Estavel)":
            self.susp_var.set(0.85); self.diff_var.set(65); self.brake_var.set(-5)
        elif mode == "Acessibilidade (Max Estabilidade)":
            self.susp_var.set(0.75); self.diff_var.set(52); self.brake_var.set(-10)

    def _start_drag(self, event):
        self._x = event.x_root - self.winfo_x()
        self._y = event.y_root - self.winfo_y()

    def _do_drag(self, event):
        self.geometry(f"+{event.x_root - self._x}+{event.y_root - self._y}")

    def save_and_apply(self):
        self.rules_data["mode"] = self.mode_var.get()

        if "suspension" not in self.rules_data:
            self.rules_data["suspension"] = {}
        for key in ["front_suspension", "rear_suspension", "front_anti_roll_bar", "rear_anti_roll_bar"]:
            if key not in self.rules_data["suspension"]:
                self.rules_data["suspension"][key] = {}
            self.rules_data["suspension"][key]["factor"] = self.susp_var.get()

        if "transmission" not in self.rules_data:
            self.rules_data["transmission"] = {}
        if "on_throttle" not in self.rules_data["transmission"]:
            self.rules_data["transmission"]["on_throttle"] = {}
        self.rules_data["transmission"]["on_throttle"]["clamp_max"] = self.diff_var.get()

        if "brakes" not in self.rules_data:
            self.rules_data["brakes"] = {}
        if "brake_pressure" not in self.rules_data["brakes"]:
            self.rules_data["brakes"]["brake_pressure"] = {}
        self.rules_data["brakes"]["brake_pressure"]["offset"] = self.brake_var.get()

        try:
            with open(config.RULES_FILE, 'w') as f:
                json.dump(self.rules_data, f, indent=2)
            transformer = AccessibilityTransformer()
            transformer.run()
            CyberDialog(self.master, "SUCESSO", "Regras salvas e aplicadas!")
            self.destroy()
        except Exception as e:
            CyberDialog(self.master, "ERRO", f"Falha ao salvar:\n{e}", error=True)


if __name__ == "__main__":
    app = ControlPanel()
    app.mainloop()
