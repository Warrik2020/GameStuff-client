import os
import zipfile
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox, QListWidgetItem
import requests
import subprocess
import json
from config.settings import SERVER_URL

class LauncherTab(QWidget):
    def __init__(self, username, password):
        super().__init__()

        self.username = username
        self.password = password

        self.setWindowTitle("Game Launcher")
        layout = QVBoxLayout()

        self.game_list = QListWidget()
        layout.addWidget(self.game_list)

        self.install_button = QPushButton("Install Selected Game", self)
        self.install_button.clicked.connect(self.on_install_game)
        layout.addWidget(self.install_button)

        self.launch_button = QPushButton("Launch Game", self)
        self.launch_button.clicked.connect(self.on_launch_game)
        layout.addWidget(self.launch_button)

        self.refresh_button = QPushButton("Refresh Library", self)
        self.refresh_button.clicked.connect(self.refresh_library)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.refresh_library()

    def refresh_library(self):
        self.game_list.clear()

        # Get user's library list
        library_res = requests.get(f"{SERVER_URL}/library/{self.username}")
        if library_res.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to fetch library")
            return

        library = library_res.json().get("library", [])

        # Get full metadata for all games
        market_res = requests.get(f"{SERVER_URL}/marketplace/games")
        if market_res.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to fetch game data")
            return

        all_games = market_res.json()

        # Filter by games in the user's library
        for game in all_games:
            if game["title"] in library:
                display_text = f"{game['title']} - v{game['version']}"
                item = QListWidgetItem(display_text)
                item.setData(1000, game)  # Store full game metadata
                self.game_list.addItem(item)

    def on_install_game(self):
        selected_game = self.game_list.currentItem().text()
        if selected_game:
            game_name = selected_game.split(" - ")[0].strip()
            zip_path = f"games/{game_name}.zip"
            extract_path = f"games/{game_name}"

            os.makedirs("games", exist_ok=True)

            download_url = f"{SERVER_URL}/games/download/{game_name}?username={self.username}&password={self.password}"
            res = requests.get(download_url, stream=True)
            if res.status_code == 200:
                with open(zip_path, "wb") as f:
                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    os.makedirs(extract_path, exist_ok=True)
                    zip_ref.extractall(extract_path)
                os.remove(zip_path)
                QMessageBox.information(self, "Success", f"Game {game_name} installed successfully to '{extract_path}'.")
            else:
                QMessageBox.critical(self, "Error", "Failed to download the game.")

    def on_launch_game(self):
        selected_game = self.game_list.currentItem().text()
        selected_item = selected_game.split(" - ")[0].strip()
        if selected_item:
            game_name = selected_item
            game_dir = f"games/{game_name}"

            launch_file = os.path.join(game_dir, "launchoptions.json")

            if not os.path.exists(launch_file):
                QMessageBox.critical(self, "Error", f"No launchoptions.json found for {game_name}.")
                return

            try:
                with open(launch_file, "r") as f:
                    launch_options = json.load(f)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read launchoptions.json:\n{e}")
                return

            exe_name = launch_options.get("executable")
            use_cli = launch_options.get("cli", False)
            cli_options = launch_options.get("cli_options", "")

            if not exe_name:
                QMessageBox.critical(self, "Error", "Executable not defined in launchoptions.json.")
                return

            exe_path = os.path.join(game_dir, exe_name)
            if not os.path.exists(exe_path):
                QMessageBox.critical(self, "Error", f"Executable not found: {exe_name}")
                return

            try:
                if use_cli:
                    subprocess.Popen([exe_path] + cli_options.split())
                else:
                    subprocess.Popen([exe_path])
                QMessageBox.information(self, "Launching", f"{game_name} is launching...")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to launch game:\n{e}")