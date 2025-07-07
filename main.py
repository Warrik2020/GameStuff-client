from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
import sys
from qasync import QEventLoop

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    import asyncio
    asyncio.set_event_loop(loop)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())