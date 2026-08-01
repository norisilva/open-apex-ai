import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os

import config
from scraper.dual_scraper import DualScraper
from transformer.accessibility_engine import AccessibilityTransformer

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.configure(state='normal')

    def write(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
        
    def flush(self):
        pass

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("F1 25 Setups Assist - Painel de Controle")
        self.geometry("450x450")
        self.configure(bg="#0f172a")
        
        # Style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        self.style.configure("TFrame", background="#0f172a")
        self.style.configure("TLabel", background="#0f172a", foreground="white", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#a855f7", background="#0f172a")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10, background="#3b82f6", foreground="white", borderwidth=0)
        self.style.map("TButton", background=[('active', '#2563eb')])
        
        self.style.configure("Secondary.TButton", background="#1e293b", foreground="white")
        self.style.map("Secondary.TButton", background=[('active', '#334155')])

        # Main Container
        self.container = tk.Frame(self, bg="#0f172a")
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # --- Tela 1: Menu ---
        self.menu_frame = ttk.Frame(self.container, style="TFrame")
        
        ttk.Label(self.menu_frame, text="F1 Setups Assist", style="Title.TLabel").pack(pady=(0, 20))
        
        self.status_var = tk.StringVar(value="Status: Pronto")
        self.status_label = ttk.Label(self.menu_frame, textvariable=self.status_var, foreground="#22c55e")
        self.status_label.pack(pady=(0, 20))
        
        self.btn_scrape = ttk.Button(self.menu_frame, text="🔄 Baixar Setups da Nuvem", command=self.run_scraper)
        self.btn_scrape.pack(fill=tk.X, pady=5)
        
        self.btn_settings = ttk.Button(self.menu_frame, text="⚙️ Configurar Perfis", command=self.open_settings)
        self.btn_settings.pack(fill=tk.X, pady=5)
        
        self.btn_overlay = ttk.Button(self.menu_frame, text="🚀 Iniciar HUD no Jogo", command=self.run_overlay)
        self.btn_overlay.pack(fill=tk.X, pady=5)
        
        footer_frame = tk.Frame(self.menu_frame, bg="#0f172a")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        ttk.Label(footer_frame, text="Ao rodar o HUD, feche o F1Laps App.", foreground="#94a3b8", font=("Segoe UI", 8)).pack(side=tk.LEFT)
        
        # --- Tela 2: Console ---
        self.console_frame = ttk.Frame(self.container, style="TFrame")
        ttk.Label(self.console_frame, text="Progresso do Robo", style="Title.TLabel").pack(pady=(0, 10))
        
        self.console_text = scrolledtext.ScrolledText(self.console_frame, wrap=tk.WORD, bg="#020617", fg="#10b981", font=("Consolas", 9), height=15, borderwidth=0)
        self.console_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.console_text.configure(state='disabled')
        
        self.btn_back = ttk.Button(self.console_frame, text="Voltar ao Menu", style="Secondary.TButton", command=self.show_menu)
        self.btn_back.pack(fill=tk.X, pady=5)
        
        self.show_menu()
        
    def show_menu(self):
        self.console_frame.pack_forget()
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_console(self):
        self.menu_frame.pack_forget()
        self.console_frame.pack(fill=tk.BOTH, expand=True)

    def run_scraper(self):
        self.show_console()
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')
        self.btn_back.config(state="disabled")
        
        def scrape_thread():
            old_stdout = sys.stdout
            sys.stdout = ConsoleRedirector(self.console_text)
            
            try:
                print("Iniciando extracao de setups da nuvem...\n")
                scraper = DualScraper()
                scraper.run()
                
                print("\nAplicando perfis matematicos e salvando...")
                transformer = AccessibilityTransformer()
                transformer.run()
                
                print("\nConcluido com sucesso! Voce ja pode voltar ao menu.")
                self.status_var.set("Status: Setups atualizados com sucesso!")
                self.status_label.config(foreground="#22c55e")
            except Exception as e:
                print(f"\nERRO NA EXTRACAO: {e}")
                self.status_var.set(f"Status: Erro na extracao.")
                self.status_label.config(foreground="#ef4444")
            finally:
                sys.stdout = old_stdout
                self.btn_back.config(state="normal")
                
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
