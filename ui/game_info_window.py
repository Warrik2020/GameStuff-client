from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import requests
from config.settings import SERVER_URL

class GameInfoWindow(QWidget):
    def __init__(self, game_data, username, password):
        super().__init__()
        self.setWindowTitle(game_data["title"])
        self.setFixedSize(400, 300)

        self.game_data = game_data
        self.username = username
        self.password = password

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"<h2>{game_data['title']}</h2>"))
        layout.addWidget(QLabel(f"<b>Developer</b><br>{game_data['developer']}"))
        layout.addWidget(QLabel(f"<b>Description</b><br>{game_data['description']}"))
        #layout.addWidget(QLabel(f"<b>Requirements:</b><br>{game_data['requirements']}"))

        add_btn = QPushButton("Add to library")
        add_btn.clicked.connect(self.add_to_library)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    def add_to_library(self):
        selected = self.game_data['title']
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a game.")
            return

        game_name = selected

        payload = {
            "username": self.username,
            "password": self.password,
            "game_name": game_name
        }

        response = requests.post(
            SERVER_URL,
            json=payload
        )

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Game added to your library!")
        else:
            error_detail = response.json().get("detail", "Failed to add game")
            if isinstance(error_detail, list):
                error_detail = "\n".join(str(item) for item in error_detail)
            QMessageBox.critical(self, "Error", error_detail)