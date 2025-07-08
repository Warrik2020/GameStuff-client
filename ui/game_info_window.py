from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import requests
from config.settings import SERVER_URL, load_settings

class GameInfoWindow(QWidget):
    def __init__(self, game_data, username, password):
        super().__init__()
        self.setWindowTitle(game_data["title"])
        self.setFixedSize(400, 300)

        self.game_data = game_data
        self.username = username
        self.password = password

        settings = load_settings()
        self.apply_theme(settings.get("dark_mode", True))

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"<h2>{game_data['title']}</h2>"))
        layout.addWidget(QLabel(f"<b>Developer:</b><br>{game_data.get('developer', 'Unknown')}"))
        layout.addWidget(QLabel(f"<b>Description:</b><br>{game_data.get('description', 'No description')}"))

        if "requirements" in game_data:
            reqs = game_data["requirements"]
            req_text = "<br>".join([f"{k}: {v}" for k, v in reqs.items()])
            layout.addWidget(QLabel(f"<b>Requirements:</b><br>{req_text}"))

        add_btn = QPushButton("Add to Library")
        add_btn.clicked.connect(self.add_to_library)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    def apply_theme(self, dark_mode_enabled):
        if dark_mode_enabled:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2e2e2e;
                    color: #ffffff;
                }
                QLineEdit, QPushButton, QListWidget, QLabel {
                    background-color: #3a3a3a;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #444;
                }
            """)
        else:
            self.setStyleSheet("")

    def add_to_library(self):
        payload = {
            "username": self.username,
            "password": self.password,
            "game_name": self.game_data["title"]
        }

        try:
            response = requests.post(f"{SERVER_URL}/library/add", json=payload)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Game added to your library!")
            elif response.status_code == 400:
                QMessageBox.warning(self, "Already Exists", "This game is already in your library.")
            else:
                try:
                    error_detail = response.json().get("detail", "Unknown error")
                except Exception:
                    error_detail = response.text or "Unknown error"
                QMessageBox.critical(self, "Error", f"Failed to add game:\n{error_detail}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Network Error", f"Could not connect to server:\n{str(e)}")