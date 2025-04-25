import requests
import os
from config.settings import DOWNLOADS_DIR, MODS_DIR

def download_file(url: str, dest_folder: str, filename: str):
    os.makedirs(dest_folder, exist_ok=True)
    path = os.path.join(dest_folder, filename)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return path
