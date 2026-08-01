import json, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.config_manager import ConfigManager

class AccessibilityTransformer:
    def __init__(self, config_manager=None):
        self.rules = config_manager.rules_data if config_manager else ConfigManager().rules_data
        
    def apply_rule(self, val, rule):
        if not rule: return val
        if "factor" in rule: val *= rule["factor"]
        if "offset" in rule: val += rule["offset"]
        if "clamp_max" in rule: val = min(val, rule["clamp_max"])
        if "clamp_min" in rule: val = max(val, rule["clamp_min"])
        if "max" in rule: val = min(val, rule["max"])
        if "min" in rule: val = max(val, rule["min"])
        return round(val) if rule.get("round", False) else (round(val, 1) if isinstance(val, float) else val)
        
    def transform_setup(self, setup: dict) -> dict:
        new_setup = {}
        for key, val in setup.items():
            if not isinstance(val, dict):
                new_setup[key] = val
                continue
                
            new_setup[key] = {}
            if self.rules.get(key) is None:
                new_setup[key] = val.copy()
                continue
                
            for p_name, p_val in val.items():
                rule = self.rules[key].get(p_name)
                new_setup[key][p_name] = self.apply_rule(p_val, rule) if rule else p_val
                    
        return new_setup
        
    def run(self):
        if not os.path.exists(config.ORIGINAL_SETUPS_FILE):
            print(f"Erro: {config.ORIGINAL_SETUPS_FILE} ausente.")
            return False
            
        try:
            with open(config.ORIGINAL_SETUPS_FILE, 'r', encoding='utf-8') as f:
                orig = json.load(f)
                
            trans = {}
            for slug, info in orig.items():
                print(f"Suavizando: {info.get('track_name', slug)}")
                trans[slug] = self.transform_setup(info)
                
            with open(config.ACCESSIBILITY_SETUPS_FILE, 'w', encoding='utf-8') as f:
                json.dump(trans, f, indent=2, ensure_ascii=False)
                
            print(f"Salvo em {config.ACCESSIBILITY_SETUPS_FILE}")
            return True
        except Exception as e:
            print(f"Erro na transformacao: {e}")
            return False

if __name__ == "__main__":
    AccessibilityTransformer().run()
