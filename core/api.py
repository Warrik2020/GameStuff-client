import requests
from config.settings import SERVER_URL

def get(endpoint: str, params: dict = None):
    try:
        res = requests.get(f"{SERVER_URL}/{endpoint}", params=params)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"[GET] Error: {e}")
        return None

def post(endpoint: str, data: dict = None):
    try:
        res = requests.post(f"{SERVER_URL}/{endpoint}", json=data)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"[POST] Error: {e}")
        return None
