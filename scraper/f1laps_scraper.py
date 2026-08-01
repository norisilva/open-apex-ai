import json
import os
import sys

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

import config
from scraper.track_catalog import TRACKS
from scraper.track_catalog import TRACKS

class F1LapsScraper:
    def __init__(self):
        self.base_url = config.F1LAPS_BASE_URL
        self.game_version = config.GAME_VERSION
    
    def scrape_setup_detail(self, html_content: str) -> dict:
        """Parse setup detail page HTML and extract values."""
        soup = BeautifulSoup(html_content, 'html.parser')
        setup_data = {}
        
        # Mapping UI section names to our JSON keys
        sections_map = {
            "Aerodynamics": "aerodynamics",
            "Transmission": "transmission",
            "Suspension Geometry": "suspension_geometry",
            "Suspension": "suspension",
            "Brakes": "brakes",
            "Tyres": "tyres"
        }
        
        # Mapping parameter names in UI to JSON keys
        param_map = {
            "Front Wing": "front_wing",
            "Rear Wing": "rear_wing",
            "Differential Adjustment On Throttle": "on_throttle",
            "Differential Adjustment Off Throttle": "off_throttle",
            "Front Camber": "front_camber",
            "Rear Camber": "rear_camber",
            "Front Toe": "front_toe",
            "Rear Toe": "rear_toe",
            "Front Suspension": "front_suspension",
            "Rear Suspension": "rear_suspension",
            "Front Anti-Roll Bar": "front_anti_roll_bar",
            "Rear Anti-Roll Bar": "rear_anti_roll_bar",
            "Front Ride Height": "front_ride_height",
            "Rear Ride Height": "rear_ride_height",
            "Break Pressure": "brake_pressure", # Typo original do F1Laps
            "Brake Pressure": "brake_pressure", # Caso o F1Laps corrija o typo
            "Front Break Bias": "front_brake_bias",
            "Front Brake Bias": "front_brake_bias",
            "Front Right Tyre Pressure": "front_right_pressure",
            "Front Left Tyre Pressure": "front_left_pressure",
            "Rear Right Tyre Pressure": "rear_right_pressure",
            "Rear Left Tyre Pressure": "rear_left_pressure",
        }

        # Find all sections (they are in divs with rounded-lg border)
        sections = soup.select("div.rounded-lg.border.bg-background")
        
        for section in sections:
            header_span = section.select_one("span.text-lg.font-medium")
            if not header_span:
                continue
                
            section_name = header_span.text.strip()
            if section_name not in sections_map:
                continue
                
            section_key = sections_map[section_name]
            setup_data[section_key] = {}
            
            # Iterate over parameters (dt for label, dd.text-right.text-base for value)
            rows = section.select("div.flex.space-x-5")
            for row in rows:
                label_el = row.select_one("dt.text-sm")
                value_el = row.select_one("dd.text-right.text-base")
                
                if label_el and value_el:
                    label = label_el.text.strip()
                    val_str = value_el.text.strip()
                    
                    if label in param_map:
                        param_key = param_map[label]
                        # Clean up value (remove %, ˚, etc)
                        clean_val = val_str.replace('%', '').replace('˚', '')
                        try:
                            # Try parsing as float first
                            parsed_val = float(clean_val)
                            # Convert to int if it's a whole number and not in geometry/tyres
                            if parsed_val.is_integer() and section_key not in ["suspension_geometry", "tyres"]:
                                parsed_val = int(parsed_val)
                        except ValueError:
                            parsed_val = clean_val
                            
                        setup_data[section_key][param_key] = parsed_val
        
        return setup_data

    def get_track_setup(self, page, slug: str) -> dict:
        """Scrape setup for a single track using an existing page."""
        track_info = TRACKS.get(slug)
        if not track_info:
            return None
            
        # Navigate to the track's setup list page (filtering by Race session)
        list_url = f"{self.base_url}/{self.game_version}/setups/{slug}/?session={config.SESSION_RACE}"
        try:
            page.goto(list_url, wait_until='domcontentloaded', timeout=45000)
        except Exception as e:
            print(f"Aviso ao carregar lista (pode ser timeout normal de trackers): {e}")
            return None
        
        # Wait for the table to load
        try:
            page.wait_for_selector("table tbody tr", timeout=10000)
        except Exception as e:
            print(f"Erro ao carregar tabela para {slug}: {e}")
            return None
        
        # Get the link to the first setup (assuming it's the top-rated/fastest)
        first_row_link = page.query_selector("table tbody tr a")
        if not first_row_link:
            print(f"Nenhum setup encontrado para {slug}.")
            return None
            
        setup_href = first_row_link.get_attribute("href")
        if not setup_href.startswith("http"):
            setup_url = f"{self.base_url}{setup_href}"
        else:
            setup_url = setup_href
            
        print(f"Extraindo setup de {setup_url}")
        try:
            page.goto(setup_url, wait_until='domcontentloaded', timeout=45000)
        except Exception as e:
            print(f"Aviso ao carregar detalhes (pode ser timeout normal de trackers): {e}")
            return None
        
        # Wait for the setup parameters to load
        try:
            page.wait_for_selector("div.rounded-lg.border.bg-background", timeout=10000)
        except Exception as e:
            print(f"Erro ao carregar detalhes do setup: {e}")
            return None
        
        html_content = page.content()
        setup_data = self.scrape_setup_detail(html_content)
        
        if not setup_data:
            return None
            
        # Add metadata
        return {
            "track_name": track_info["name"],
            "circuit": track_info["circuit"],
            "udp_track_id": track_info["udp_id"],
            "source_url": setup_url,
            "session_type": "race",
            **setup_data
        }

    def run(self, tracks_to_scrape: list = None):
        """Main scraping loop for selected tracks."""
        if tracks_to_scrape is None:
            tracks_to_scrape = list(TRACKS.keys())
            
        print(f"Iniciando extracao para as pistas: {', '.join(tracks_to_scrape)}")
        all_setups = {}
        
        with sync_playwright() as p:
            # We use headless=True to run invisibly. If blocked by Cloudflare, change to headless=False
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            for slug in tracks_to_scrape:
                print(f"Processando {slug}...")
                setup_data = self.get_track_setup(page, slug)
                if setup_data:
                    all_setups[slug] = setup_data
                
            browser.close()
            
        if not all_setups:
            print("Nenhum setup foi extraido. O arquivo original nao sera modificado.")
            return

        # Save to file
        with open(config.ORIGINAL_SETUPS_FILE, "w", encoding="utf-8") as f:
            json.dump(all_setups, f, indent=2, ensure_ascii=False)
        print(f"Extracao concluida! Dados salvos em {config.ORIGINAL_SETUPS_FILE}")

if __name__ == "__main__":
    # Test execution for Monza only
    scraper = F1LapsScraper()
    scraper.run(["monza"])
