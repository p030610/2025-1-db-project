from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel, QLineEdit
)
import psycopg2
from UserWindow import UserWindow
from ManagerWindow import ManagerWindow
from LoginWindow import LoginWindow
from DB_CONFIG import DB_CONFIG

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("등록")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("아이디")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("비밀번호")

        self.register_complete_btn = QPushButton("등록 마치기")
        self.register_complete_btn.clicked.connect(self.add_new_user)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_complete_btn)

        self.setLayout(layout)

    def add_new_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO "User" (username, password_hash, role)
                VALUES ('%s', '%s', 'user');
            """, (username, password))

            conn.close()

            QMessageBox.information(self, "성공", f"가입 성공. 로그인 해주세요.")
            self.open_login_window()

        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def open_login_window(self):
        self.next = LoginWindow()
        self.next.show()
        self.close()
    

        
        