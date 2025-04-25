from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTabWidget
from config.settings import load_settings
from ui.marketplace_tab import MarketplaceTab
from ui.workshop_tab import WorkshopTab
from ui.launcher_tab import LauncherTab
from ui.settings_tab import SettingsTab

class MainWindow(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.setWindowTitle("Game Client")
        self.setFixedSize(600, 400)
        settings = load_settings()
        self.apply_theme(settings.get("dark_mode", True))

        self.username = username
        self.password = password

        tabs = QTabWidget()

        tabs.addTab(MarketplaceTab(self.username, self.password), "Marketplace")
        tabs.addTab(WorkshopTab(), "Workshop")
        tabs.addTab(LauncherTab(self.username, self.password), "Launcher")
        tabs.addTab(SettingsTab(), "Settings")

        self.setCentralWidget(tabs)

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
            
            QTabWidget::pane {
                border: 1px solid #444;
                background: #2b2b2b;
            }

            QTabBar::tab {
                background: #2b2b2b;
                color: #ccc;
                padding: 6px;
                border: 1px solid #444;
                border-bottom: none;
            }

            QTabBar::tab:selected {
                background: #3b3b3b;
                color: white;
            }

            QTabBar::tab:hover {
                background: #444;
            }
        """)
        else:
            self.setStyleSheet("")