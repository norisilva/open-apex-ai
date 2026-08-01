from bs4 import BeautifulSoup

def scrape_f1laps_setup_detail(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')
    setup_data = {}
    
    sec_map = {
        "Aerodynamics": "aerodynamics", "Transmission": "transmission",
        "Suspension Geometry": "suspension_geometry", "Suspension": "suspension",
        "Brakes": "brakes", "Tyres": "tyres"
    }
    
    p_map = {
        "Front Wing": "front_wing", "Rear Wing": "rear_wing",
        "Differential Adjustment On Throttle": "on_throttle", "Differential Adjustment Off Throttle": "off_throttle",
        "Front Camber": "front_camber", "Rear Camber": "rear_camber",
        "Front Toe": "front_toe", "Rear Toe": "rear_toe",
        "Front Suspension": "front_suspension", "Rear Suspension": "rear_suspension",
        "Front Anti-Roll Bar": "front_anti_roll_bar", "Rear Anti-Roll Bar": "rear_anti_roll_bar",
        "Front Ride Height": "front_ride_height", "Rear Ride Height": "rear_ride_height",
        "Break Pressure": "brake_pressure", "Brake Pressure": "brake_pressure",
        "Front Break Bias": "front_brake_bias", "Front Brake Bias": "front_brake_bias",
        "Front Right Tyre Pressure": "front_right_pressure", "Front Left Tyre Pressure": "front_left_pressure",
        "Rear Right Tyre Pressure": "rear_right_pressure", "Rear Left Tyre Pressure": "rear_left_pressure",
    }

    for section in soup.select("div.rounded-lg.border.bg-background"):
        h_span = section.select_one("span.text-lg.font-medium")
        if not h_span or h_span.text.strip() not in sec_map: continue
            
        s_key = sec_map[h_span.text.strip()]
        setup_data[s_key] = {}
        
        for row in section.select("div.flex.space-x-5"):
            l_el, v_el = row.select_one("dt.text-sm"), row.select_one("dd.text-right.text-base")
            if l_el and v_el and l_el.text.strip() in p_map:
                p_key = p_map[l_el.text.strip()]
                clean_val = v_el.text.strip().replace('%', '').replace('˚', '')
                try:
                    val = float(clean_val)
                    if val.is_integer() and s_key not in ["suspension_geometry", "tyres"]: val = int(val)
                except ValueError: val = clean_val
                setup_data[s_key][p_key] = val
                
    return setup_data
