import os

# F1Laps Configuration
F1LAPS_BASE_URL = "https://www.f1laps.com"
SRS_BASE_URL = "https://simracingsetup.com"
GAME_VERSION = "f1-25"  # Conforme solicitado, usando a versao F1 25
SESSION_RACE = 5
SESSION_TIME_TRIAL = 6

# Telemetry Configuration
UDP_PORT = 20777

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ORIGINAL_SETUPS_FILE = os.path.join(DATA_DIR, "setups_originais.json")
ACCESSIBILITY_SETUPS_FILE = os.path.join(DATA_DIR, "setups_acessibilidade.json")
RULES_FILE = os.path.join(DATA_DIR, "rules.json")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)
