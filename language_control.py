import json
import subprocess

class LanguageController:
    def __init__(self):
        self.language = "en"  # Bahasa default (Inggris)
        self.load_translations()

    def load_translations(self):
        try:
            with open("language.json", "r") as file:
                self.translations = json.load(file)
        except FileNotFoundError:
            print("File 'language.json' not found. Please create it with translations.")

    def set_language(self, lang):
        if lang in self.translations:
            self.language = lang
            print("Language set to:", lang)
        else:
            print("Language not supported:", lang)

    def translate(self, key):
        if key in self.translations.get(self.language, {}):
            return self.translations[self.language][key]
        else:
            return key

# Contoh penggunaan
if __name__ == "__main__":
    controller = LanguageController()
    controller.set_language("ru")  # Ganti bahasa ke Indonesia
    print(controller.translate("welcome"))


def select_language():
    return None