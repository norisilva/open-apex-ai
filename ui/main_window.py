import tkinter as tk
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.theme import *
from ui.widgets import CyberTitleBar
from ui.dialogs import CyberDialog
from ui.menu_frame import MenuFrame
from ui.console_frame import ConsoleFrame, ConsoleRedirector
from ui.settings_window import SettingsWindow
from scraper.dual_scraper import DualScraper
from transformer.accessibility_engine import AccessibilityTransformer
from ui.window_manager import WindowManager

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.geometry("420x520+100+80")
        self.configure(bg=BG_DEEP)
        self.wm_attributes("-topmost", False)

        outer = tk.Frame(self, bg=CYAN, padx=1, pady=1)
        outer.pack(fill=tk.BOTH, expand=True)

        inner = tk.Frame(outer, bg=BG_DEEP, padx=1, pady=1)
        inner.pack(fill=tk.BOTH, expand=True)

        self.title_bar = CyberTitleBar(inner, title="F1 SETUPS ASSIST // v2.0", on_close=self.destroy, on_minimize=self.iconify)
        self.title_bar.pack(fill=tk.X)

        self.main_panel = tk.Frame(inner, bg=BG_PANEL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)
        self.container = tk.Frame(self.main_panel, bg=BG_PANEL)
        self.container.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        self.menu_frame = MenuFrame(self.container, self.run_scraper, self.open_settings, self.run_smart_hud, self.run_auto_config)
        self.console_frame = ConsoleFrame(self.container, self.show_menu)
        
        self.window_manager = WindowManager(self, hotkey='f4')
            
        self.show_menu()

    def destroy(self):
        if hasattr(self, 'window_manager'):
            self.window_manager.destroy()
        super().destroy()

    def show_menu(self):
        self.console_frame.stop_blink()
        self.console_frame.pack_forget()
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

    def show_console(self):
        self.menu_frame.pack_forget()
        self.console_frame.pack(fill=tk.BOTH, expand=True)
        self.console_frame.start_blink()

    def run_scraper(self):
        self.show_console()
        self.console_frame.text.configure(state='normal')
        self.console_frame.text.delete(1.0, tk.END)
        self.console_frame.text.configure(state='disabled')
        self.console_frame.set_back_enabled(False)

        def scrape_thread():
            old_stdout = sys.stdout
            sys.stdout = ConsoleRedirector(self.console_frame.text)
            try:
                print("╔══════════════════════════════════════╗")
                print("║  INICIANDO EXTRACAO DE SETUPS        ║")
                print("╚══════════════════════════════════════╝\n")
                DualScraper().run()
                print("\n[ OK ] Aplicando perfis matematicos...")
                AccessibilityTransformer().run()
                self.menu_frame.set_status("SETUPS ATUALIZADOS!", NEON_GREEN)
            except Exception as e:
                print(f"\n[ERRO] {e}")
                self.menu_frame.set_status("ERRO NA EXTRACAO", MAGENTA)
            finally:
                sys.stdout = old_stdout
                self.console_frame.set_back_enabled(True)
                self.console_frame.stop_blink()

        threading.Thread(target=scrape_thread, daemon=True).start()

    def open_settings(self):
        try:
            SettingsWindow(self)
        except Exception as e:
            CyberDialog(self, "ERRO", f"Falha ao abrir configuracoes:\n{e}", error=True)

    def run_smart_hud(self):
        try:
            from overlay.overlay_manager import HUDManager
            self.withdraw()
            app = HUDManager(parent=self)
            app.run()
            self.wait_window(app.root)
            self.deiconify()
        except Exception as e:
            CyberDialog(self, "ERRO", f"Erro ao iniciar o HUD Inteligente:\n{e}", error=True)

    def run_auto_config(self):
        try:
            from telemetry.game_config import GameConfigurator
            configurator = GameConfigurator()
            result = configurator.configure_all_games()
            if result.get("success"):
                CyberDialog(self, "SUCESSO", result.get("msg"), error=False)
            else:
                CyberDialog(self, "ERRO", result.get("msg"), error=True)
        except Exception as e:
            CyberDialog(self, "ERRO", f"Falha na auto-configuracao:\n{e}", error=True)
