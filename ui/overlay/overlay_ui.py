import os, sys, json, tkinter as tk
from tkinter import ttk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.scraper.track_catalog import TRACKS
from core.telemetry.listener import TelemetryListener
from ui.overlay.theme import setup_overlay_style, setup_window_properties

class OverlayApp:
    def __init__(self, parent=None, managed=False):
        if parent is None:
            self.root, self.owns_root = tk.Tk(), True
        else:
            self.root, self.owns_root = tk.Toplevel(parent), False
            
        self.managed = managed
        setup_window_properties(self.root, "F1 Setups Assist - Overlay", "380x600+50+50")
        self.style = setup_overlay_style()
        self.setups = self.load_setups()
        self.current_track = None
        self.is_visible = True
        
        self.build_ui()
        self.telemetry = None if self.managed else TelemetryListener(
            config.UDP_PORT, self.on_track_detected, self.update_status, self.on_speed_changed)
        
    def load_setups(self):
        f = config.ACCESSIBILITY_SETUPS_FILE if os.path.exists(config.ACCESSIBILITY_SETUPS_FILE) else config.ORIGINAL_SETUPS_FILE
        return json.load(open(f, 'r', encoding='utf-8')) if os.path.exists(f) else {}
        
    def build_ui(self):
        main = ttk.Frame(self.root, padding="10")
        main.pack(fill=tk.BOTH, expand=True)
        head = ttk.Frame(main)
        head.pack(fill=tk.X, pady=(0, 10))
        self.status_lbl = ttk.Label(head, text="Aguardando telemetria...", foreground="yellow")
        self.status_lbl.pack(side=tk.TOP, anchor=tk.W)
        self.track_lbl = ttk.Label(head, text="Nenhuma pista", style="Header.TLabel")
        self.track_lbl.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.content = ttk.Frame(main)
        self.content.pack(fill=tk.BOTH, expand=True)
        ttk.Label(self.content, text="Entre na pista no F1 25\npara exibir o setup aqui.").pack(pady=50)
        
    def update_status(self, msg, color):
        self.root.after(0, lambda: self.status_lbl.configure(text=msg, foreground=color))
        
    def on_speed_changed(self, speed):
        def toggle():
            if speed > 2 and self.is_visible:
                self.root.withdraw(); self.is_visible = False
            elif speed <= 2 and not self.is_visible:
                self.root.deiconify(); self.root.attributes("-topmost", True); self.is_visible = True
        self.root.after(0, toggle)
        
    def on_track_detected(self, track_id):
        track_slug = next((s for s, i in TRACKS.items() if i["udp_id"] == track_id), None)
        if not track_slug:
            return self.root.after(0, lambda: self.track_lbl.configure(text=f"ID {track_id} nao mapeada"))
        if track_slug not in self.setups:
            return self.root.after(0, lambda: self.track_lbl.configure(text=f"Sem setup {TRACKS[track_slug]['name']}"))
        if self.current_track != track_slug:
            self.current_track = track_slug
            self.root.after(0, lambda ts=track_slug: self.render_setup(ts))
            
    def render_row(self, p, lbl, val):
        r = ttk.Frame(p)
        r.pack(fill=tk.X, pady=1)
        ttk.Label(r, text=lbl, style="Param.TLabel").pack(side=tk.LEFT)
        ttk.Label(r, text=str(val), style="Value.TLabel").pack(side=tk.RIGHT)
        
    def render_setup(self, track_slug):
        setup = self.setups[track_slug]
        self.track_lbl.configure(text=setup["track_name"])
        for w in self.content.winfo_children(): w.destroy()
        
        sections = [
            ("Aerodinamica", "aerodynamics", {"front_wing": "Front Wing", "rear_wing": "Rear Wing"}),
            ("Transmissao", "transmission", {"on_throttle": "Diff On-Throttle", "off_throttle": "Diff Off-Throttle"}),
            ("Suspensao", "suspension", {"front_suspension": "Front Sus", "rear_suspension": "Rear Sus", "front_anti_roll_bar": "Front ARB", "rear_anti_roll_bar": "Rear ARB", "front_ride_height": "Front H", "rear_ride_height": "Rear H"}),
            ("Freios", "brakes", {"brake_pressure": "Pressure", "front_brake_bias": "Bias"}),
            ("Pneus", "tyres", {"front_right_pressure": "FR", "front_left_pressure": "FL", "rear_right_pressure": "RR", "rear_left_pressure": "RL"})
        ]
        
        for t, k, p in sections:
            if k in setup and setup[k]:
                ttk.Label(self.content, text=t, style="Section.TLabel").pack(anchor=tk.W)
                for pk, lbl in p.items():
                    if pk in setup[k]: self.render_row(self.content, lbl, setup[k][pk])
                    
    def run(self):
        if self.telemetry: self.telemetry.start()
        def on_closing():
            if self.telemetry: self.telemetry.stop()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        if self.owns_root: self.root.mainloop()
