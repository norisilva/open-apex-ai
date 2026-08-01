import os
from config import SRS_BASE_URL, GAME_VERSION
from scraper.track_catalog import TRACKS

class SRSScraper:
    def __init__(self):
        self.output_file = os.path.join(os.path.dirname(__file__), "..", "data", "setups_originais.json")

    def get_track_setup(self, page, track_slug):
        track_info = TRACKS.get(track_slug)
        if not track_info or not track_info.get("srs_slug"): return None

        srs_slug = track_info["srs_slug"]
        url = f"{SRS_BASE_URL}/setups/{GAME_VERSION}/{srs_slug}/"
        print(f"Buscando setup fallback (SRS) para {track_slug}...")
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            links = page.locator("a[href*='/setups/f1-25-setups/']").all() or page.locator(".car-setup-archive-box a").all()
            
            setup_url = next((l.get_attribute("href") for l in links if l.get_attribute("href") and "/setups/f1-25" in l.get_attribute("href") and "tracks" not in l.get_attribute("href")), None)
            if not setup_url:
                print(f"Link do setup nao encontrado para {track_slug} no SRS")
                return None
                
            print(f"Extraindo setup de {setup_url}")
            page.goto(setup_url, wait_until="domcontentloaded", timeout=15000)
            
            parts = page.locator(".setup-part-100, .setup-part-50").all()
            raw_data = {}
            for part in parts:
                try:
                    name = part.locator(".setup-part-name").inner_text().strip().replace(":", "")
                    value = part.locator(".setup-part-number").inner_text().strip().replace("%", "")
                    raw_data[name] = float(value) if "." in value else int(value)
                except: continue

            if not raw_data: return None

            setup = {
                "aerodynamics": {"front_wing": raw_data.get("Front Wing Aero", 0), "rear_wing": raw_data.get("Rear Wing Aero", 0)},
                "transmission": {"on_throttle": raw_data.get("Differential Adjustment On Throttle", 0), "off_throttle": raw_data.get("Differential Adjustment Off Throttle", 0)},
                "suspension_geometry": {"front_camber": raw_data.get("Front Camber", 0.0), "rear_camber": raw_data.get("Rear Camber", 0.0), "front_toe": raw_data.get("Front Toe", 0.0), "rear_toe": raw_data.get("Rear Toe", 0.0)},
                "suspension": {"front_suspension": raw_data.get("Front Suspension", 0), "rear_suspension": raw_data.get("Rear Suspension", 0), "front_anti_roll_bar": raw_data.get("Front Anti-Roll Bar", 0), "rear_anti_roll_bar": raw_data.get("Rear Anti-Roll Bar", 0), "front_ride_height": raw_data.get("Front Ride Height", 0), "rear_ride_height": raw_data.get("Rear Ride Height", 0)},
                "brakes": {"brake_pressure": raw_data.get("Brake Pressure", 0), "front_brake_bias": raw_data.get("Brake Bias", 0)},
                "tyres": {"front_right_pressure": raw_data.get("Front Right Tyre Pressure", 0.0), "front_left_pressure": raw_data.get("Front Left Tyre Pressure", 0.0), "rear_right_pressure": raw_data.get("Rear Right Tyre Pressure", 0.0), "rear_left_pressure": raw_data.get("Rear Left Tyre Pressure", 0.0)}
            }
            if "Engine Braking" in raw_data: setup["transmission"]["engine_braking"] = raw_data["Engine Braking"]
                
            return {"track_name": track_info["name"], "circuit": track_info["circuit"], "udp_track_id": track_info["udp_id"], "source_url": setup_url, "session_type": "race", **setup}
        except Exception as e:
            print(f"Erro ao carregar SRS para {track_slug}: {e}")
            return None
