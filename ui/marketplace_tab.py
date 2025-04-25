from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from ui.game_info_window import GameInfoWindow
import requests
from config.settings import SERVER_URL

class MarketplaceTab(QWidget):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Available Games"))

        self.games_list = QListWidget()
        self.games_list.itemDoubleClicked.connect(self.show_game_info)
        layout.addWidget(self.games_list)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_games)
        layout.addWidget(refresh_btn)

        add_to_library_btn = QPushButton("Add to Library")
        add_to_library_btn.clicked.connect(self.add_to_library)
        layout.addWidget(add_to_library_btn)

        self.setLayout(layout)
        self.load_games()

    def load_games(self):
        self.games_list.clear()
        try:
            res = requests.get(f"{SERVER_URL}/marketplace/games")
            if res.status_code == 200:
                for game in res.json():
                    item = QListWidgetItem(f"{game['title']} - {game['description']}")
                    item.setData(1000, game)
                    self.games_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load games:\n{e}")

    def add_to_library(self):
        selected = self.games_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a game.")
            return

        game = selected.data(1000)
        game_name = game["title"]

        payload = {
            "username": self.username,
            "password": self.password,
            "game_name": game_name
        }

        response = requests.post(
            f"{SERVER_URL}/library/add",
            json=payload
        )

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Game added to your library!")
        else:
            error_detail = response.json().get("detail", "Failed to add game")
            if isinstance(error_detail, list):
                error_detail = "\n".join(str(item) for item in error_detail)
            QMessageBox.critical(self, "Error", error_detail)
    
    def show_game_info(self, item):
        game = item.data(1000)
        self.game_info_window = GameInfoWindow(game, self.username, self.password)
        self.game_info_window.show()