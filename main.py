import os
import sys

# Add parent directory to path to import config
import config
from scraper.dual_scraper import DualScraper
from transformer.accessibility_engine import AccessibilityTransformer

def main():
    print("========================================")
    print(" F1 SETUPS ASSIST - ACESSIBILIDADE      ")
    print("========================================")
    print("1. Extrair setups do F1Laps (Scrape)")
    print("2. Aplicar motor de transformacao")
    print("3. Iniciar Telemetria e Overlay")
    print("4. Executar fluxo completo (1, 2 e 3)")
    print("0. Sair")
    print("========================================")
    
    choice = input("Escolha uma opcao: ")
    
    if choice == '1':
        scraper = DualScraper()
        # Executa a extracao para todas as pistas do catalogo
        scraper.run()
        
    elif choice == '2':
        transformer = AccessibilityTransformer()
        transformer.run()
        
    elif choice == '3':
        print("Iniciando overlay e servidor de telemetria...")
        try:
            # Importa aqui para nao travar a execucao caso falte dependencia grafica (Tkinter)
            from overlay.overlay_ui import OverlayApp
            app = OverlayApp()
            app.run()
        except ImportError as e:
            print(f"Erro ao carregar o modulo de interface: {e}")
            
    elif choice == '4':
        scraper = DualScraper()
        scraper.run()
        
        transformer = AccessibilityTransformer()
        if transformer.run():
            try:
                from overlay.overlay_ui import OverlayApp
                app = OverlayApp()
                app.run()
            except ImportError as e:
                print(f"Erro ao carregar o modulo de interface: {e}")
                
    elif choice == '0':
        print("Saindo...")
        sys.exit(0)
    else:
        print("Opcao invalida.")
        
if __name__ == "__main__":
    main()
