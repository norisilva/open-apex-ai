import json
import os
import sys

# Ajusta o sys.path para garantir que config root possa ser lido
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class ConfigManager:
    def __init__(self):
        self.rules_file = config.RULES_FILE
        self.rules_data = {}
        self.load()

    def load(self):
        if os.path.exists(self.rules_file):
            try:
                with open(self.rules_file, 'r', encoding='utf-8') as f:
                    self.rules_data = json.load(f)
            except Exception as e:
                print(f"Erro ao ler rules.json: {e}")
                self.rules_data = {}
        else:
            self.rules_data = {}

    def get_language(self):
        return self.rules_data.get("language", "pt_br")

    def get_mode(self):
        return self.rules_data.get("mode", "Acessibilidade (Max Estabilidade)")

    def get_suspension_factor(self):
        return self.rules_data.get("suspension", {}).get("front_suspension", {}).get("factor", 0.75)

    def get_diff_max(self):
        return self.rules_data.get("transmission", {}).get("on_throttle", {}).get("clamp_max", 52)

    def get_brake_offset(self):
        return self.rules_data.get("brakes", {}).get("brake_pressure", {}).get("offset", -5)

    def save(self, mode, susp, diff, brake, language="pt_br"):
        self.rules_data["mode"] = mode
        self.rules_data["language"] = language

        if "suspension" not in self.rules_data:
            self.rules_data["suspension"] = {}
            
        for key in ["front_suspension", "rear_suspension", "front_anti_roll_bar", "rear_anti_roll_bar"]:
            if key not in self.rules_data["suspension"]:
                self.rules_data["suspension"][key] = {}
            self.rules_data["suspension"][key]["factor"] = susp

        if "transmission" not in self.rules_data:
            self.rules_data["transmission"] = {}
        if "on_throttle" not in self.rules_data["transmission"]:
            self.rules_data["transmission"]["on_throttle"] = {}
        self.rules_data["transmission"]["on_throttle"]["clamp_max"] = diff

        if "brakes" not in self.rules_data:
            self.rules_data["brakes"] = {}
        if "brake_pressure" not in self.rules_data["brakes"]:
            self.rules_data["brakes"]["brake_pressure"] = {}
        self.rules_data["brakes"]["brake_pressure"]["offset"] = brake

        with open(self.rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.rules_data, f, indent=2)
