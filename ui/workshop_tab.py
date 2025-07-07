from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class WorkshopTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Workshop - Mods & Community Content (Not Finished)"))
        self.setLayout(layout)