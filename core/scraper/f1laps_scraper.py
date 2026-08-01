import json, os, sys
from playwright.sync_api import sync_playwright
import config
from core.scraper.track_catalog import TRACKS
from core.scraper.html_parser import scrape_f1laps_setup_detail

class F1LapsScraper:
    def __init__(self):
        self.base_url, self.game_version = config.F1LAPS_BASE_URL, config.GAME_VERSION
    
    def get_track_setup(self, page, slug: str) -> dict:
        track_info = TRACKS.get(slug)
        if not track_info: return None
            
        url = f"{self.base_url}/{self.game_version}/setups/{slug}/?session={config.SESSION_RACE}"
        try: page.goto(url, wait_until='domcontentloaded', timeout=45000)
        except Exception as e: return None
        
        try: page.wait_for_selector("table tbody tr", timeout=10000)
        except: return None
        
        first_row_link = page.query_selector("table tbody tr a")
        if not first_row_link: return None
            
        href = first_row_link.get_attribute("href")
        setup_url = href if href.startswith("http") else f"{self.base_url}{href}"
            
        print(f"Extraindo setup de {setup_url}")
        try: page.goto(setup_url, wait_until='domcontentloaded', timeout=45000)
        except: return None
        
        try: page.wait_for_selector("div.rounded-lg.border.bg-background", timeout=10000)
        except: return None
        
        setup_data = scrape_f1laps_setup_detail(page.content())
        if not setup_data: return None
            
        return {
            "track_name": track_info["name"], "circuit": track_info["circuit"],
            "udp_track_id": track_info["udp_id"], "source_url": setup_url,
            "session_type": "race", **setup_data
        }

    def run(self, tracks_to_scrape: list = None):
        if tracks_to_scrape is None: tracks_to_scrape = list(TRACKS.keys())
        print(f"Iniciando extracao para as pistas: {', '.join(tracks_to_scrape)}")
        all_setups = {}
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36")
            page = context.new_page()
            
            for slug in tracks_to_scrape:
                print(f"Processando {slug}...")
                setup_data = self.get_track_setup(page, slug)
                if setup_data: all_setups[slug] = setup_data
                
            browser.close()
            
        if not all_setups:
            print("Nenhum setup foi extraido.")
            return

        with open(config.ORIGINAL_SETUPS_FILE, "w", encoding="utf-8") as f:
            json.dump(all_setups, f, indent=2, ensure_ascii=False)
        print(f"Dados salvos em {config.ORIGINAL_SETUPS_FILE}")
