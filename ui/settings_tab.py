from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
from config.settings import load_settings, save_settings

class SettingsTab(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()

        self.download_dir_input = QLineEdit()
        self.dark_mode_checkbox = QCheckBox("Dark Mode")

        layout.addWidget(QLabel("Download Directory:"))
        layout.addWidget(self.download_dir_input)
        layout.addWidget(self.dark_mode_checkbox)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_existing_settings()

    def load_existing_settings(self):
        settings = load_settings()
        self.download_dir_input.setText(settings.get("download_dir", "games"))
        self.dark_mode_checkbox.setChecked(settings.get("dark_mode", True))

    def save_settings(self):
        settings = {
            "download_dir": self.download_dir_input.text(),
            "dark_mode": self.dark_mode_checkbox.isChecked()
        }
        save_settings(settings)
        
        QMessageBox.information(self, "Settings", "Settings saved successfully!")
