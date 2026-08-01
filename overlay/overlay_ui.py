import os
import sys
import json
import tkinter as tk
from tkinter import ttk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scraper.track_catalog import TRACKS
from overlay.telemetry_listener import TelemetryListener

class OverlayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("F1 Setups Assist - Acessibilidade")
        
        # Always on top and semi-transparent
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.90)
        self.root.configure(bg="#1E1E1E")
        
        # Window size and position
        self.root.geometry("380x600+50+50")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("TFrame", background="#1E1E1E")
        self.style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF")
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground="#FFBB00")
        self.style.configure("Section.TLabel", font=("Segoe UI", 10, "bold"), foreground="#64C4FF", padding=(0, 10, 0, 5))
        self.style.configure("Param.TLabel", font=("Segoe UI", 9))
        self.style.configure("Value.TLabel", font=("Segoe UI", 9, "bold"), foreground="#52E252")
        
        # Setup Data
        self.setups = self.load_setups()
        self.current_track = None
        
        # UI Elements
        self.build_ui()
        
        # Telemetry Listener
        self.telemetry = TelemetryListener(
            port=config.UDP_PORT, 
            callback=self.on_track_detected,
            status_callback=self.update_status
        )
        
    def load_setups(self):
        if not os.path.exists(config.ACCESSIBILITY_SETUPS_FILE):
            print("Setups de acessibilidade nao encontrados. Usando originais ou vazio.")
            file_to_load = config.ORIGINAL_SETUPS_FILE
        else:
            file_to_load = config.ACCESSIBILITY_SETUPS_FILE
            
        if os.path.exists(file_to_load):
            with open(file_to_load, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
        
    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header (Status & Track)
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_lbl = ttk.Label(header_frame, text="Aguardando telemetria...", foreground="yellow")
        self.status_lbl.pack(side=tk.TOP, anchor=tk.W)
        
        self.track_lbl = ttk.Label(header_frame, text="Nenhuma pista detectada", style="Header.TLabel")
        self.track_lbl.pack(side=tk.TOP, anchor=tk.W, pady=5)
        
        # Values Frame (Scrollable could be added, but we'll use simple pack for now)
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize empty state
        self.render_empty_state()
        
    def render_empty_state(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.content_frame, text="Entre na pista no F1 25\npara exibir o setup aqui.").pack(pady=50)
        
    def update_status(self, msg, color):
        self.root.after(0, lambda: self.status_lbl.configure(text=msg, foreground=color))
        
    def on_track_detected(self, track_id):
        # Look up track slug by id
        track_slug = None
        for slug, info in TRACKS.items():
            if info["udp_id"] == track_id:
                track_slug = slug
                break
                
        if not track_slug:
            # We detected a track but it's not in our catalog
            self.root.after(0, lambda: self.track_lbl.configure(text=f"Pista ID {track_id} nao mapeada"))
            return
            
        if track_slug not in self.setups:
            self.root.after(0, lambda: self.track_lbl.configure(text=f"Sem setup p/ {TRACKS[track_slug]['name']}"))
            return
            
        if self.current_track != track_slug:
            self.current_track = track_slug
            self.root.after(0, lambda ts=track_slug: self.render_setup(ts))
            
    def render_row(self, parent, label, value):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=1)
        ttk.Label(row, text=label, style="Param.TLabel").pack(side=tk.LEFT)
        ttk.Label(row, text=str(value), style="Value.TLabel").pack(side=tk.RIGHT)
        
    def render_setup(self, track_slug):
        setup = self.setups[track_slug]
        self.track_lbl.configure(text=setup["track_name"])
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Helper to render sections
        def render_section(title, key, param_labels):
            if key not in setup or not setup[key]: return
            ttk.Label(self.content_frame, text=title, style="Section.TLabel").pack(anchor=tk.W)
            for param_key, label in param_labels.items():
                if param_key in setup[key]:
                    self.render_row(self.content_frame, label, setup[key][param_key])
        
        # Define layout
        render_section("Aerodinâmica", "aerodynamics", {
            "front_wing": "Front Wing", "rear_wing": "Rear Wing"
        })
        
        render_section("Transmissão", "transmission", {
            "on_throttle": "Diff On-Throttle", "off_throttle": "Diff Off-Throttle"
        })
        
        render_section("Suspensão", "suspension", {
            "front_suspension": "Front Sus", "rear_suspension": "Rear Sus",
            "front_anti_roll_bar": "Front ARB", "rear_anti_roll_bar": "Rear ARB",
            "front_ride_height": "Front Height", "rear_ride_height": "Rear Height"
        })
        
        render_section("Freios", "brakes", {
            "brake_pressure": "Pressure", "front_brake_bias": "Bias"
        })
        
        render_section("Pneus", "tyres", {
            "front_right_pressure": "Front Right", "front_left_pressure": "Front Left",
            "rear_right_pressure": "Rear Right", "rear_left_pressure": "Rear Left"
        })

    def run(self):
        self.telemetry.start()
        
        # Test hook - uncomment to simulate detecting Monza after 2 seconds
        # self.root.after(2000, lambda: self.on_track_detected(11))
        
        def on_closing():
            self.telemetry.stop()
            self.root.destroy()
            
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = OverlayApp()
    app.run()
