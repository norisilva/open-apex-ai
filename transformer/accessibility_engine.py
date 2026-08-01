import json
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class AccessibilityTransformer:
    def __init__(self):
        self.rules = self.load_rules()
        
    def load_rules(self):
        if os.path.exists(config.RULES_FILE):
            try:
                with open(config.RULES_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao ler {config.RULES_FILE}: {e}")
        return {}
        
    def apply_rule(self, value, rule_config):
        """Aplica uma unica regra a um valor especifico."""
        if not rule_config:
            return value
            
        new_val = value
        
        # Aplicar fator multiplicativo (ex: 0.75 para -25%)
        if "factor" in rule_config:
            new_val = new_val * rule_config["factor"]
            
        # Aplicar offset aditivo/subtrativo (ex: -0.5 para PSI)
        if "offset" in rule_config:
            new_val = new_val + rule_config["offset"]
            
        # Limitar valores maximos e minimos (clamping)
        if "clamp_max" in rule_config:
            new_val = min(new_val, rule_config["clamp_max"])
            
        if "clamp_min" in rule_config:
            new_val = max(new_val, rule_config["clamp_min"])
            
        if "max" in rule_config:
            new_val = min(new_val, rule_config["max"])
            
        if "min" in rule_config:
            new_val = max(new_val, rule_config["min"])
            
        # Arredondar se necessario
        if rule_config.get("round", False):
            new_val = round(new_val)
        elif isinstance(new_val, float):
            # Arredondar para 1 casa decimal por padrao em floats
            new_val = round(new_val, 1)
            
        return new_val
        
    def transform_setup(self, setup: dict) -> dict:
        """Aplica transformacoes em um setup completo."""
        transformed_setup = {}
        
        for key, val in setup.items():
            # Preservar chaves que nao sao dicionarios de configs (metadata)
            if not isinstance(val, dict):
                transformed_setup[key] = val
                continue
                
            section = key
            section_data = val
            transformed_setup[section] = {}
            
            # Se nao tem regras (None), apenas copia os valores
            if self.rules.get(section) is None:
                for param_name, param_value in section_data.items():
                    transformed_setup[section][param_name] = param_value
                continue
                
            # Aplicar regras parametrizadas
            for param_name, param_value in section_data.items():
                rule = self.rules[section].get(param_name)
                
                if rule:
                    transformed_val = self.apply_rule(param_value, rule)
                    transformed_setup[section][param_name] = transformed_val
                else:
                    # Copia parametro se nao houver regra especifica
                    transformed_setup[section][param_name] = param_value
                    
        return transformed_setup
        
    def run(self):
        """Transforma o arquivo JSON inteiro e salva o resultado."""
        if not os.path.exists(config.ORIGINAL_SETUPS_FILE):
            print(f"Erro: Arquivo original {config.ORIGINAL_SETUPS_FILE} não encontrado.")
            return False
            
        try:
            with open(config.ORIGINAL_SETUPS_FILE, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
                
            transformed_data = {}
            for track_slug, setup_info in original_data.items():
                print(f"Aplicando suavizacao para pista: {setup_info.get('track_name', track_slug)}")
                transformed_data[track_slug] = self.transform_setup(setup_info)
                
            with open(config.ACCESSIBILITY_SETUPS_FILE, 'w', encoding='utf-8') as f:
                json.dump(transformed_data, f, indent=2, ensure_ascii=False)
                
            print(f"Transformacao concluida! Dados salvos em {config.ACCESSIBILITY_SETUPS_FILE}")
            return True
            
        except Exception as e:
            print(f"Erro durante a transformacao: {e}")
            return False

if __name__ == "__main__":
    transformer = AccessibilityTransformer()
    transformer.run()
