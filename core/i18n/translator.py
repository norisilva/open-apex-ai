import json
import os

class I18n:
    _locale = "pt_br"
    _strings = {}

    @classmethod
    def load_locale(cls, locale):
        cls._locale = locale
        path = os.path.join(os.path.dirname(__file__), 'locales', f"{locale}.json")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                cls._strings = json.load(f)
        except Exception as e:
            print(f"[i18n] Erro ao carregar idioma '{locale}': {e}")
            cls._strings = {}

    @classmethod
    def get(cls, key, **kwargs):
        text = cls._strings.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text

# Atalho global
_ = I18n.get
