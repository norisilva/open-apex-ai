import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ui.main_window import ControlPanel
from core.config_manager import ConfigManager
from core.i18n.translator import I18n

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    cfg = ConfigManager()
    I18n.load_locale(cfg.get_language())
    app = ControlPanel()
    app.mainloop()
