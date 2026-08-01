import tkinter as tk
import traceback
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.theme import *
from ui.widgets import neon_button
from ui.dialogs import CyberDialog
from core.config_manager import ConfigManager
from core.transformer.accessibility_engine import AccessibilityTransformer
from core.i18n.translator import _

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg=MAGENTA)
        self.transient(parent)
        
        px = max(0, parent.winfo_x() + (parent.winfo_width() // 2) - 200)
        py = max(0, parent.winfo_y() + (parent.winfo_height() // 2) - 270)
        self.geometry(f"400x540+{px}+{py}")

        try:
            self._build_ui(parent)
            self.update_idletasks()
            self.attributes('-topmost', True)
            self.grab_set()
        except Exception as e:
            self.destroy()
            raise e

    def _build_ui(self, parent):
        inner = tk.Frame(self, bg=BG_PANEL)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        title_bar = tk.Frame(inner, bg=BG_DEEP, height=36)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Frame(title_bar, bg=MAGENTA, height=2).pack(fill=tk.X, side=tk.TOP)
        title_content = tk.Frame(title_bar, bg=BG_DEEP)
        title_content.pack(fill=tk.BOTH, expand=True)
        tk.Label(title_content, text=_("config_profile"), bg=BG_DEEP, fg=MAGENTA, font=(FONT_MONO, 9, "bold")).pack(side=tk.LEFT, padx=10)
        close_btn = tk.Label(title_content, text="âœ•", bg=BG_DEEP, fg=GRAY, font=(FONT_MONO, 11), cursor="hand2", padx=10)
        close_btn.pack(side=tk.RIGHT)
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=MAGENTA))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=GRAY))
        close_btn.bind("<Button-1>", lambda e: self.destroy())

        self._x = self._y = 0
        for w in [title_bar, title_content]:
            w.bind("<ButtonPress-1>", self._start_drag)
            w.bind("<B1-Motion>", self._do_drag)

        content = tk.Frame(inner, bg=BG_PANEL, padx=20, pady=16)
        content.pack(fill=tk.BOTH, expand=True)

        self.config_mgr = ConfigManager()
        self.current_mode = self.config_mgr.get_mode()
        self.current_lang = self.config_mgr.get_language()

        tk.Label(content, text=_("lang_label"), bg=BG_PANEL, fg=MAGENTA, font=(FONT_MONO, 8, "bold")).pack(anchor="w", pady=(0, 4))
        self.lang_var = tk.StringVar(value=self.current_lang)
        
        lang_frame = tk.Frame(content, bg=MAGENTA, padx=1, pady=1)
        lang_frame.pack(fill=tk.X, pady=(0, 14))
        self.lang_combo = tk.OptionMenu(lang_frame, self.lang_var, "en", "pt_br", "es", "de", "hi", "ar")
        self.lang_combo.config(bg=BG_CARD, fg=MAGENTA, font=(FONT_MONO, 9), activebackground=BG_CARD, activeforeground=MAGENTA, highlightthickness=0, bd=0, relief="flat", indicatoron=True)
        self.lang_combo["menu"].config(bg=BG_CARD, fg=MAGENTA, font=(FONT_MONO, 9), activebackground=MAGENTA, activeforeground=BG_DEEP)
        self.lang_combo.pack(fill=tk.X)

        tk.Label(content, text=_("driving_mode"), bg=BG_PANEL, fg=MAGENTA, font=(FONT_MONO, 8, "bold")).pack(anchor="w", pady=(0, 4))
        self.mode_var = tk.StringVar(value=self.current_mode)
        self.modes = [_("mode_esports"), _("mode_gamepad"), _("mode_accessibility"), _("mode_custom")]

        mode_frame = tk.Frame(content, bg=MAGENTA, padx=1, pady=1)
        mode_frame.pack(fill=tk.X, pady=(0, 14))
        self.mode_combo = tk.OptionMenu(mode_frame, self.mode_var, *self.modes, command=self._on_mode_change)
        self.mode_combo.config(bg=BG_CARD, fg=MAGENTA, font=(FONT_MONO, 9), activebackground=BG_CARD, activeforeground=MAGENTA, highlightthickness=0, bd=0, relief="flat", indicatoron=True)
        self.mode_combo["menu"].config(bg=BG_CARD, fg=MAGENTA, font=(FONT_MONO, 9), activebackground=MAGENTA, activeforeground=BG_DEEP)
        self.mode_combo.pack(fill=tk.X)

        self.susp_var  = tk.DoubleVar(value=self.config_mgr.get_suspension_factor())
        self.diff_var  = tk.IntVar(value=self.config_mgr.get_diff_max())
        self.brake_var = tk.IntVar(value=self.config_mgr.get_brake_offset())

        self._make_slider(content, _("lbl_suspension"),       self.susp_var,  0.5,  1.0)
        self._make_slider(content, _("lbl_diff_max"), self.diff_var,  50,   100)
        self._make_slider(content, _("lbl_brake_offset"),   self.brake_var, -15,  0)

        self.hotkey_var = tk.StringVar(value=self.config_mgr.get_tyre_hotkey())
        tk.Label(content, text=_("lbl_tyre_hotkey"), bg=BG_PANEL, fg=MAGENTA, font=(FONT_MONO, 8, "bold")).pack(anchor="w", pady=(8, 4))
        entry = tk.Entry(content, textvariable=self.hotkey_var, bg=BG_CARD, fg=CYAN, font=(FONT_MONO, 9), bd=0, highlightthickness=0, insertbackground=CYAN)
        entry.pack(fill=tk.X, pady=(0, 6), ipady=4)

        tk.Frame(content, bg=GRAY, height=1).pack(fill=tk.X, pady=12)
        btn_row = tk.Frame(content, bg=BG_PANEL)
        btn_row.pack(fill=tk.X)

        btn_cancel, _btn1 = neon_button(btn_row, _("btn_cancel"), self.destroy, color=GRAY)
        btn_cancel.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))

        btn_save, _btn2 = neon_button(btn_row, _("btn_save_close"), self.save_and_apply, color=MAGENTA)
        btn_save.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))

    def _make_slider(self, parent, label, variable, from_, to_):
        tk.Label(parent, text=label, bg=BG_PANEL, fg=CYAN, font=(FONT_MONO, 7, "bold")).pack(anchor="w", pady=(8, 2))
        slider_frame = tk.Frame(parent, bg=BG_PANEL)
        slider_frame.pack(fill=tk.X)
        s = tk.Scale(
            slider_frame, variable=variable, from_=from_, to=to_, orient=tk.HORIZONTAL,
            bg=BG_CARD, fg=CYAN, troughcolor=BG_DEEP, activebackground=CYAN, highlightthickness=0, bd=0,
            sliderlength=18, showvalue=True, font=(FONT_MONO, 7), resolution=0.01 if isinstance(variable, tk.DoubleVar) else 1
        )
        s.pack(fill=tk.X)
        s.bind("<ButtonRelease-1>", lambda e: self.mode_var.set(_("mode_custom")))

    def _on_mode_change(self, mode):
        if mode == _("mode_esports"):
            self.susp_var.set(1.0); self.diff_var.set(100); self.brake_var.set(0)
        elif mode == _("mode_gamepad"):
            self.susp_var.set(0.85); self.diff_var.set(65); self.brake_var.set(-5)
        elif mode == _("mode_accessibility"):
            self.susp_var.set(0.75); self.diff_var.set(52); self.brake_var.set(-10)

    def _start_drag(self, event):
        self._x = event.x_root - self.winfo_x()
        self._y = event.y_root - self.winfo_y()

    def _do_drag(self, event):
        self.geometry(f"+{event.x_root - self._x}+{event.y_root - self._y}")

    def save_and_apply(self):
        try:
            self.config_mgr.save(self.mode_var.get(), self.susp_var.get(), self.diff_var.get(), self.brake_var.get(), self.lang_var.get(), self.hotkey_var.get())
            transformer = AccessibilityTransformer()
            transformer.run()
            CyberDialog(self.master, _("dialog_success"), _("msg_saved"))
            self.destroy()
        except Exception as e:
            CyberDialog(self.master, _("dialog_error"), _("msg_save_error", error=e), error=True)
