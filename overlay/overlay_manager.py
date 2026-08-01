import os, sys, tkinter as tk, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from telemetry.listener import TelemetryListener
from overlay.overlay_ui import OverlayApp
from overlay.overlay_tyre import TyreOverlayApp

class HUDManager:
    def __init__(self, parent=None):
        if parent is None:
            self.root, self.owns_root = tk.Tk(), True
        else:
            self.root, self.owns_root = tk.Toplevel(parent), False
            
        self.root.withdraw()
        
        self.setup_hud = OverlayApp(parent=self.root, managed=True)
        self.tyre_hud = TyreOverlayApp(parent=self.root, managed=True)
        
        if self.tyre_hud.is_visible: self.tyre_hud.toggle_visibility()
            
        self.telemetry = TelemetryListener(
            port=config.UDP_PORT,
            callback=self.setup_hud.on_track_detected,
            status_callback=self.setup_hud.update_status,
            speed_callback=self.on_speed_changed,
            lap_callback=self.tyre_hud.on_lap_changed,
            wear_callback=self.on_wear_changed,
            distance_callback=self.on_distance_changed
        )
        self.speed = 0.0
        self.tyre_alert = False
        self.lap_alert = False
        self.lap_timer = None
        
        try:
            keyboard.unhook_all()
            keyboard.on_press_key("f8", lambda e: self.root.after(0, self.tyre_hud.toggle_visibility))
        except Exception as e: print("Erro atalho F8:", e)
            
    def show_tyre_hud(self, auto_hide_ms=None):
        if not self.tyre_hud.is_visible: self.tyre_hud.toggle_visibility()
        if auto_hide_ms:
            if self.lap_timer: self.root.after_cancel(self.lap_timer)
            self.lap_timer = self.root.after(auto_hide_ms, self.hide_tyre_hud)
            
    def hide_tyre_hud(self):
        if self.tyre_hud.is_visible and not self.tyre_alert: self.tyre_hud.toggle_visibility()

    def on_speed_changed(self, speed):
        self.speed = speed
        self.setup_hud.on_speed_changed(speed)
        
    def on_wear_changed(self, wear_data):
        self.tyre_hud.on_wear_changed(wear_data)
        if max(wear_data) >= 50.0 and not self.tyre_alert:
            self.tyre_alert = True
            if not self.tyre_hud.is_visible: self.root.after(0, self.tyre_hud.toggle_visibility)
                
    def on_distance_changed(self, lap_dist, track_length):
        if track_length <= 0: return
        pct = (lap_dist / track_length) * 100.0
        if (0 <= pct <= 5) or (45 <= pct <= 50):
            if not self.lap_alert:
                self.lap_alert = True
                self.root.after(0, lambda: self.show_tyre_hud(5000))
        else: self.lap_alert = False

    def run(self):
        self.telemetry.start()
        def on_closing():
            self.telemetry.stop()
            try: keyboard.unhook_all()
            except: pass
            self.root.destroy()
            if self.owns_root: sys.exit(0)
            
        self.setup_hud.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.tyre_hud.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.setup_hud.run()
        self.tyre_hud.run()
        if self.owns_root: self.root.mainloop()
