import os
import json
from playwright.sync_api import sync_playwright

from scraper.f1laps_scraper import F1LapsScraper
from scraper.srs_scraper import SRSScraper
from scraper.track_catalog import TRACKS

class DualScraper:
    def __init__(self):
        self.output_file = os.path.join(os.path.dirname(__file__), "..", "data", "setups_originais.json")
        self.f1laps = F1LapsScraper()
        self.srs = SRSScraper()

    def run(self, tracks_to_scrape=None):
        if tracks_to_scrape is None:
            tracks_to_scrape = list(TRACKS.keys())

        print(f"Iniciando extracao para as pistas: {', '.join(tracks_to_scrape)}")
        
        # Le o arquivo existente para nao sobrescrever pistas que ja temos
        all_setups = {}
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r') as f:
                    all_setups = json.load(f)
            except Exception:
                pass

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            for track_slug in tracks_to_scrape:
                print(f"Processando {track_slug}...")
                
                # Tenta o Primario (F1Laps)
                setup_data = self.f1laps.get_track_setup(page, track_slug)
                
                if not setup_data or "aerodynamics" not in setup_data:
                    # Falhou no primario, tenta o Secundario (SimRacingSetup)
                    print(f"F1Laps falhou para {track_slug}, acionando fallback (SimRacingSetup)...")
                    setup_data = self.srs.get_track_setup(page, track_slug)
                
                if setup_data:
                    all_setups[track_slug] = setup_data
                else:
                    print(f"Nenhum setup encontrado para {track_slug} em nenhuma das fontes.")

            browser.close()

        # Salva apenas se extraiu algo para nao apagar dados bons antigos
        if all_setups:
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, 'w') as f:
                json.dump(all_setups, f, indent=4)
            print(f"Extracao concluida! Dados salvos em {self.output_file}")
        else:
            print("Extracao falhou completamente. Arquivo original nao modificado.")
