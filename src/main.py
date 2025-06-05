import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from DatabaseManager import DatabaseManager
from ui.LoginWindow import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = DatabaseManager()
    if not db.connect(dbname="postgres", user="", password=""):
        QMessageBox.critical(None, "Database Error", "Could not connect to PostgreSQL.")
        sys.exit(1)

    window = LoginWindow()
    window.show()
    app.exec()
    db.close()