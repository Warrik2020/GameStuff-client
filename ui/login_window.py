from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from core.auth import login, register
from core.session import save_session, load_session
from ui.main_window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.on_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.on_register)
        layout.addWidget(self.register_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.main_window = None  # store main window instance here

        session = load_session()
        if session:
            self.username_input.setText(session["username"])
            self.password_input.setText(session["password"])
            QTimer.singleShot(100, lambda: self.on_login(auto=True))

    def on_login(self, auto=False):
        username = self.username_input.text()
        password = self.password_input.text()

        response = login(username, password)
        if response and response.get("msg") == "Login successful":
            if not auto:
                save_session(username, password)
            self.main_window = MainWindow(username, password)
            self.main_window.show()
            self.close()  # hide login window
        else:
            print("Login failed")

    def on_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        response = register(username, password)
        if response and response.get("msg") == "User registered successfully":
            print("Registration successful")
        else:
            print("Registration failed")