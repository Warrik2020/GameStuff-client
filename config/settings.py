import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER_URL = "https://gamestuff-server.onrender.com"
DOWNLOADS_DIR = os.path.join(BASE_DIR, "..", "games")
MODS_DIR = os.path.join(BASE_DIR, "..", "mods")
SETTINGS_PATH = 'settings.json'

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(data, f, indent=4)