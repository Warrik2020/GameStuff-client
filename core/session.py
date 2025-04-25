import os
import json
SESSION_FILE = os.path.join(os.path.expanduser("~"), ".gameclient_session.json")

def save_session(username: str, password: str):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username, "password": password}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)