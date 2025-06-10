from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel, QLineEdit
)
from PyQt6.QtGui import QGuiApplication
import psycopg2

from DB_CONFIG import DB_CONFIG

class ReviewPopup(QWidget):
    def __init__(self, store_name):
        super().__init__()
        self.store_name=store_name
        self.setWindowTitle("%s 의 위생평가", store_name)

        self.setGeometry(100, 100, 300, 600)

        layout = QVBoxLayout()
        self.table=QTableWidget()

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
                VALUES (%s, %s, 'user');
            """, (username, password))

            conn.commit()

            cursor.close()
            conn.close()

            QMessageBox.information(self, "성공", f"가입 성공. 로그인 해주세요.")
            self.open_login_window()

        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def open_login_window(self):
        from ui.LoginWindow import LoginWindow
        self.next = LoginWindow()
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate position to center the window
        x = (screen_width - self.next.width()) // 2
        y = (screen_height - self.next.height()) // 2

        self.next.move(x, y)
        self.next.show()
        self.close()
    

        
        