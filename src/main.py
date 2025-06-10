import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QGuiApplication
from DatabaseManager import DatabaseManager
from ui.LoginWindow import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = DatabaseManager()
    if not db.connect(dbname="postgres", user="", password=""):
        QMessageBox.critical(None, "Database Error", "Could not connect to PostgreSQL.")
        sys.exit(1)

    window = LoginWindow()
    screen = QGuiApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()

    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    # Calculate position to center the window
    x = (screen_width - window.width()) // 2
    y = (screen_height - window.height()) // 2

    window.move(x, y)
    window.show()
    
    app.exec()
    db.close()