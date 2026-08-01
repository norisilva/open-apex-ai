import os
import shutil
import xml.etree.ElementTree as ET

class GameConfigurator:
    def __init__(self):
        user_profile = os.environ.get('USERPROFILE')
        self.my_games_dir = os.path.join(user_profile, 'Documents', 'My Games')

    def configure_all_games(self):
        """
        Busca todas as pastas F1 (F1 22, F1 23, F1 24, F1 25) e configura o XML.
        Retorna dicionario com resultado.
        """
        if not os.path.exists(self.my_games_dir):
            return {"success": False, "msg": "Pasta 'My Games' nao encontrada."}

        games_found = []
        games_configured = []
        already_configured = 0

        try:
            for folder_name in os.listdir(self.my_games_dir):
                if folder_name.startswith("F1 ") and folder_name[3:].isdigit():
                    games_found.append(folder_name)
        except Exception as e:
            return {"success": False, "msg": f"Erro ao acessar My Games: {str(e)}"}
            
        if not games_found:
            return {"success": False, "msg": "Nenhum jogo da franquia F1 encontrado."}

        for game in games_found:
            config_path = os.path.join(self.my_games_dir, game, 'hardwaresettings', 'hardware_settings_config.xml')
            if os.path.exists(config_path):
                try:
                    res = self._configure_file(config_path, game)
                    if res == "modified":
                        games_configured.append(game)
                    elif res == "already_configured":
                        already_configured += 1
                except Exception as e:
                    print(f"Erro ao configurar {game}: {e}")

        if games_configured:
            return {"success": True, "msg": f"Configurado com sucesso: {', '.join(games_configured)}"}
        elif already_configured > 0:
            return {"success": True, "msg": "Os jogos encontrados ja estavam configurados corretamente!"}
        else:
            return {"success": False, "msg": "Nenhum arquivo de configuracao foi encontrado."}

    def _configure_file(self, file_path, game_name):
        """Modifica o XML dinamicamente."""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        modified = False
        motion = root.find('motion')
        if motion is not None:
            udp = motion.find('udp')
            if udp is not None:
                game_year = game_name.replace("F1 ", "20") # F1 24 -> 2024
                
                configs = {
                    "enabled": "true",
                    "ip": "127.0.0.1",
                    "port": "20777",
                    "sendRate": "60",
                    "format": game_year
                }
                
                for key, val in configs.items():
                    if udp.get(key) != val:
                        udp.set(key, val)
                        modified = True

        if modified:
            backup_path = file_path + ".bak"
            if not os.path.exists(backup_path):
                shutil.copy2(file_path, backup_path)
                
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            return "modified"
            
        return "already_configured"
