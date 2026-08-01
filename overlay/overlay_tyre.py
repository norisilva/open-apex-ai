import os, sys, tkinter as tk, keyboard
from tkinter import ttk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from telemetry.listener import TelemetryListener
from overlay.tyre_predictor import TyrePredictor
from overlay.theme import setup_overlay_style, setup_window_properties

class TyreOverlayApp:
    def __init__(self, parent=None, managed=False):
        if parent is None: self.root, self.owns_root = tk.Tk(), True
        else: self.root, self.owns_root = tk.Toplevel(parent), False
            
        self.managed = managed
        setup_window_properties(self.root, "F1 Setups Assist - Pneus", "320x280+50+700")
        self.style = setup_overlay_style()
        self.is_visible = True
        
        if not self.managed:
            try: keyboard.on_press_key("f8", self.toggle_visibility)
            except: pass
            
        self.predictor = TyrePredictor()
        self.build_ui()
        
        self.telemetry = None if self.managed else TelemetryListener(
            config.UDP_PORT, None, lap_callback=self.on_lap_changed, wear_callback=self.on_wear_changed)
        
    def toggle_visibility(self, e=None):
        if self.is_visible: self.root.withdraw()
        else: self.root.deiconify(); self.root.attributes("-topmost", True)
        self.is_visible = not self.is_visible
            
    def build_ui(self):
        main = ttk.Frame(self.root, padding="10")
        main.pack(fill=tk.BOTH, expand=True)
        hdr = ttk.Frame(main)
        hdr.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(hdr, text="ANALISE DE PNEUS [F8 ocultar]", style="Header.TLabel").pack(anchor=tk.W)
        self.status_lbl = ttk.Label(hdr, text="Aguardando volta completa...", foreground="gray")
        self.status_lbl.pack(anchor=tk.W)
        
        self.data_frame = ttk.Frame(main)
        self.data_frame.pack(fill=tk.BOTH, expand=True)
        self.lbl_current = self.add_row("Desgaste Atual (Pior Pneu):", "--")
        self.lbl_next = self.add_row("Proxima Volta (+1):", "--")
        self.lbl_in5 = self.add_row("Daqui a 5 Voltas:", "--")
        self.lbl_end = self.add_row("Final da Corrida:", "--")
        ttk.Frame(self.data_frame, height=2).pack(fill=tk.X, pady=10)
        self.lbl_pit = self.add_row("Pit Stop Sugerido:", "--", True)
        
    def add_row(self, label_text, value_text, is_crit=False):
        row = ttk.Frame(self.data_frame)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text=label_text, style="Data.TLabel").pack(side=tk.LEFT)
        val_lbl = ttk.Label(row, text=value_text, style="Crit.TLabel" if is_crit else "Warn.TLabel")
        val_lbl.pack(side=tk.RIGHT)
        return val_lbl
        
    def on_lap_changed(self, curr_lap, total_laps):
        self.predictor.update_lap(curr_lap, total_laps)
        self.update_ui()
        
    def on_wear_changed(self, wear_data):
        self.predictor.update_wear(wear_data)
        worst = max(wear_data)
        c = "white" if worst <= 50 else ("#FFCC00" if worst <= 70 else "#FF3333")
        self.root.after(0, lambda: self.lbl_current.configure(text=f"{worst:.1f}%", foreground=c))
        
    def update_ui(self):
        p = self.predictor.get_predictions()
        if not p: return
        def _set():
            if self.predictor.total_laps > 0:
                self.status_lbl.configure(text=f"Volta {self.predictor.current_lap} / {self.predictor.total_laps} (Gasto: {p['worst_rate']:.1f}%/v)")
            else: self.status_lbl.configure(text=f"Volta {self.predictor.current_lap} (Gasto: {p['worst_rate']:.1f}%/v)")
            self.lbl_next.configure(text=f"{p['next_lap']:.1f}%")
            self.lbl_in5.configure(text=f"{p['in_5_laps']:.1f}%")
            self.lbl_end.configure(text=f"{p['end_race']:.1f}%")
            self.lbl_pit.configure(text=f"{p['suggested_pit']}")
        self.root.after(0, _set)
        
    def run(self):
        if self.telemetry: self.telemetry.start()
        def on_closing():
            if self.telemetry: self.telemetry.stop()
            if not self.managed: 
                try: keyboard.unhook_all()
                except: pass
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        if self.owns_root: self.root.mainloop()
