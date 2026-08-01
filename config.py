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
import sys
import shutil

if getattr(sys, 'frozen', False):
    BUNDLED_DIR = sys._MEIPASS
    USER_APP_DATA = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'OpenApexAI')
else:
    BUNDLED_DIR = os.path.dirname(os.path.abspath(__file__))
    USER_APP_DATA = BUNDLED_DIR

USER_DATA_DIR = os.path.join(USER_APP_DATA, "data")
BUNDLED_DATA_DIR = os.path.join(BUNDLED_DIR, "data")

os.makedirs(USER_DATA_DIR, exist_ok=True)

ORIGINAL_SETUPS_FILE = os.path.join(USER_DATA_DIR, "setups_originais.json")
ACCESSIBILITY_SETUPS_FILE = os.path.join(USER_DATA_DIR, "setups_acessibilidade.json")
RULES_FILE = os.path.join(USER_DATA_DIR, "rules.json")

# Copia arquivos default embutidos para a pasta do usuario (persistente) se ainda nao existirem
for fname in ["setups_originais.json", "setups_acessibilidade.json"]:
    user_file = os.path.join(USER_DATA_DIR, fname)
    bundled_file = os.path.join(BUNDLED_DATA_DIR, fname)
    if not os.path.exists(user_file) and os.path.exists(bundled_file):
        try:
            shutil.copy2(bundled_file, user_file)
        except Exception:
            pass
