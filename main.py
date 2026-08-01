import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os

import config
from scraper.dual_scraper import DualScraper
from transformer.accessibility_engine import AccessibilityTransformer

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("F1 25 Setups Assist - Painel de Controle")
        self.geometry("450x450")
        self.configure(bg="#0f172a")
        
        # Style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        self.style.configure("TLabel", background="#0f172a", foreground="white", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#a855f7")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10, background="#3b82f6", foreground="white")
        self.style.map("TButton", background=[('active', '#2563eb')])
        
        self.style.configure("Secondary.TButton", background="#1e293b", foreground="white")
        self.style.map("Secondary.TButton", background=[('active', '#334155')])

        # Main Frame
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        ttk.Label(main_frame, text="F1 Setups Assist", style="Title.TLabel").pack(pady=(0, 20))
        
        # Status Label
        self.status_var = tk.StringVar(value="Status: Pronto")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="#22c55e")
        self.status_label.pack(pady=(0, 20))
        
        # Buttons
        self.btn_scrape = ttk.Button(main_frame, text="🔄 Baixar Setups da Nuvem", command=self.run_scraper)
        self.btn_scrape.pack(fill=tk.X, pady=5)
        
        self.btn_settings = ttk.Button(main_frame, text="⚙️ Configurar Acessibilidade", command=self.open_settings)
        self.btn_settings.pack(fill=tk.X, pady=5)
        
        self.btn_overlay = ttk.Button(main_frame, text="🚀 Iniciar HUD no Jogo", command=self.run_overlay)
        self.btn_overlay.pack(fill=tk.X, pady=5)
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg="#0f172a")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        ttk.Label(footer_frame, text="Ao rodar o HUD, feche o F1Laps App.", foreground="#94a3b8", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        
    def run_scraper(self):
        self.btn_scrape.config(state="disabled")
        self.status_var.set("Status: Baixando setups (isso pode demorar uns minutos)...")
        self.status_label.config(foreground="#eab308")
        
        def scrape_thread():
            try:
                scraper = DualScraper()
                scraper.run()
                
                transformer = AccessibilityTransformer()
                transformer.run()
                
                self.status_var.set("Status: Setups baixados e suavizados com sucesso!")
                self.status_label.config(foreground="#22c55e")
                messagebox.showinfo("Sucesso", "Setups foram extraidos e as regras aplicadas com sucesso!")
            except Exception as e:
                self.status_var.set(f"Status: Erro na extracao.")
                self.status_label.config(foreground="#ef4444")
                messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
            finally:
                self.btn_scrape.config(state="normal")
                
        threading.Thread(target=scrape_thread, daemon=True).start()

    def open_settings(self):
        SettingsWindow(self)

    def run_overlay(self):
        try:
            from overlay.overlay_ui import OverlayApp
            
            # Como o overlay tem seu proprio mainloop, precisamos minimiza o painel
            self.iconify()
            
            app = OverlayApp()
            app.run()
            
            # Ao fechar o overlay, restaura
            self.deiconify()
        except ImportError as e:
            messagebox.showerror("Erro", f"Erro ao iniciar o overlay: {e}")

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuracoes de Perfil e Acessibilidade")
        self.geometry("400x450")
        self.configure(bg="#0f172a")
        self.transient(parent)
        self.grab_set()
        
        # Carregar rules atuais
        self.rules_data = {}
        if os.path.exists(config.RULES_FILE):
            try:
                with open(config.RULES_FILE, 'r') as f:
                    self.rules_data = json.load(f)
            except:
                pass
                
        self.current_mode = self.rules_data.get("mode", "Acessibilidade (Max Estabilidade)")
        
        # Fallback values se o json estiver vazio
        susp_factor = 0.75
        diff_max = 52
        brake_offset = -5
        
        try:
            susp_factor = self.rules_data.get("suspension", {}).get("front_suspension", {}).get("factor", 0.75)
            diff_max = self.rules_data.get("transmission", {}).get("on_throttle", {}).get("clamp_max", 52)
            brake_offset = self.rules_data.get("brakes", {}).get("brake_pressure", {}).get("offset", -5)
        except:
            pass
            
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Perfil de Conducao", style="Title.TLabel").pack(pady=(0, 10))
        
        # Dropdown Modos
        self.mode_var = tk.StringVar(value=self.current_mode)
        self.modes = ["Esports (Original)", "Gamepad (Estavel)", "Acessibilidade (Max Estabilidade)", "Personalizado"]
        self.mode_combo = ttk.Combobox(main_frame, textvariable=self.mode_var, values=self.modes, state="readonly")
        self.mode_combo.pack(fill=tk.X, pady=(0, 15))
        self.mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)
        
        # Slider Suspensao (Macia <-> Dura)
        ttk.Label(main_frame, text="Rigidez da Suspensao").pack(anchor="w")
        self.susp_var = tk.DoubleVar(value=susp_factor)
        self.susp_slider = ttk.Scale(main_frame, from_=0.5, to=1.0, variable=self.susp_var, orient=tk.HORIZONTAL)
        self.susp_slider.pack(fill=tk.X, pady=(5, 15))
        self.susp_slider.bind("<ButtonRelease-1>", lambda e: self.set_custom_mode())
        
        # Slider Diferencial (Solto <-> Travado)
        # Max varia de 50 (Travado) a 100 (Original)
        ttk.Label(main_frame, text="Diferencial Maximo (On Throttle)").pack(anchor="w")
        self.diff_var = tk.IntVar(value=diff_max)
        self.diff_slider = ttk.Scale(main_frame, from_=50, to=100, variable=self.diff_var, orient=tk.HORIZONTAL)
        self.diff_slider.pack(fill=tk.X, pady=(5, 15))
        self.diff_slider.bind("<ButtonRelease-1>", lambda e: self.set_custom_mode())
        
        # Slider Freio (-15 a 0)
        ttk.Label(main_frame, text="Pressao do Freio (Reducao)").pack(anchor="w")
        self.brake_var = tk.IntVar(value=brake_offset)
        self.brake_slider = ttk.Scale(main_frame, from_=-15, to=0, variable=self.brake_var, orient=tk.HORIZONTAL)
        self.brake_slider.pack(fill=tk.X, pady=(5, 15))
        self.brake_slider.bind("<ButtonRelease-1>", lambda e: self.set_custom_mode())
        
        # Botoes
        btn_frame = tk.Frame(main_frame, bg="#0f172a")
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(btn_frame, text="Salvar e Aplicar", command=self.save_and_apply).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Cancelar", style="Secondary.TButton", command=self.destroy).pack(side=tk.RIGHT)
        
    def set_custom_mode(self):
        self.mode_var.set("Personalizado")
        
    def on_mode_change(self, event):
        mode = self.mode_var.get()
        if mode == "Esports (Original)":
            self.susp_var.set(1.0)
            self.diff_var.set(100)
            self.brake_var.set(0)
        elif mode == "Gamepad (Estavel)":
            self.susp_var.set(0.85)
            self.diff_var.set(65)
            self.brake_var.set(-5)
        elif mode == "Acessibilidade (Max Estabilidade)":
            self.susp_var.set(0.75)
            self.diff_var.set(52)
            self.brake_var.set(-10)
        
    def save_and_apply(self):
        # Atualizar os dados
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
        
        # Salvar JSON
        try:
            with open(config.RULES_FILE, 'w') as f:
                json.dump(self.rules_data, f, indent=2)
                
            # Re-aplicar regras nos setups existentes
            transformer = AccessibilityTransformer()
            transformer.run()
            
            messagebox.showinfo("Sucesso", "Regras salvas e aplicadas aos setups salvos!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

if __name__ == "__main__":
    app = ControlPanel()
    app.mainloop()
