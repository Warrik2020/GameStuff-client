from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QCheckBox, QMessageBox, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal, Qt
from config.settings import load_settings, save_settings

DEFAULT_DOWNLOAD_DIR = "games"
DEFAULT_DARK_MODE = True


class SettingsTab(QWidget):
    settings_changed = pyqtSignal(dict)

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Settings")
        self.init_ui()
        self.load_existing_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # === Download Directory ===
        dir_label = QLabel("Download Directory:")
        dir_label.setStyleSheet("font-weight: bold;")
        self.download_dir_input = QLineEdit()
        self.download_dir_input.setPlaceholderText("Choose or enter a download folder...")

        browse_button = QPushButton("Browse")
        browse_button.setFixedWidth(80)
        browse_button.clicked.connect(self.browse_folder)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.download_dir_input)
        dir_layout.addWidget(browse_button)

        layout.addWidget(dir_label)
        layout.addLayout(dir_layout)

        # === Dark Mode Toggle ===
        self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.setStyleSheet("padding: 5px;")
        self.dark_mode_checkbox.setToolTip("Switch UI theme (applies immediately)")

        self.dark_mode_checkbox.toggled.connect(self.preview_theme)

        layout.addWidget(self.dark_mode_checkbox)

        # === Save Button ===
        self.save_button = QPushButton("Save Settings")
        self.save_button.setFixedHeight(40)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #357ab8;
            }
        """)
        self.save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.save_button)

        # === Add stretch to push everything up ===
        layout.addStretch()

        self.setLayout(layout)

    def load_existing_settings(self):
        settings = load_settings()
        self.download_dir_input.setText(settings.get("download_dir", DEFAULT_DOWNLOAD_DIR))
        self.dark_mode_checkbox.setChecked(settings.get("dark_mode", DEFAULT_DARK_MODE))

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if folder:
            self.download_dir_input.setText(folder)

    def save_settings(self):
        settings = {
            "download_dir": self.download_dir_input.text().strip(),
            "dark_mode": self.dark_mode_checkbox.isChecked()
        }

        save_settings(settings)

        if self.main_window:
            self.main_window.apply_theme(settings["dark_mode"])

        self.settings_changed.emit(settings)

        QMessageBox.information(self, "Settings Saved", "Your settings were saved successfully.")

    def preview_theme(self, enabled):
        if self.main_window:
            self.main_window.apply_theme(enabled)
