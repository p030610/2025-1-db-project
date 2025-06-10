from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel, QLineEdit
)
from PyQt6.QtGui import QGuiApplication
import psycopg2
from ui.UserWindow import UserWindow
from ui.ManagerWindow import ManagerWindow
from ui.RegisterWindow import RegisterWindow
from DB_CONFIG import DB_CONFIG

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("아이디")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("비밀번호")

        self.login_btn = QPushButton("로그인")
        self.login_btn.clicked.connect(self.check_login)

        self.register_btn = QPushButton("등록")
        self.register_btn.clicked.connect(self.register)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT user_id, role FROM "User"
                WHERE username = %s AND password_hash = %s
            """, (username, password))

            result = cursor.fetchone()
            conn.close()

            if result:
                user_id, role = result
                role_text=""
                if role=="admin":
                    role_text="관리자"
                elif role=="user":
                    role_text="일반 사용자"
                    
                QMessageBox.information(self, "성공", f"{role_text} 로그인 성공")
                self.open_main_window(user_id, role)
            else:
                QMessageBox.warning(self, "실패", "아이디 또는 비밀번호가 틀렸습니다.")

        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def register(self):
        self.register_window = RegisterWindow()
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate position to center the window
        x = (screen_width - self.register_window.width()) // 2
        y = (screen_height - self.register_window.height()) // 2
        self.register_window.move(x,y)
        self.register_window.show()
        self.close()

    def open_main_window(self, user_id, role):
        if role=="admin":
            self.main = ManagerWindow(user_id, role)
            
            self.close()

        elif role=="user":
            self.main = UserWindow(user_id, role)
            self.close()

        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate position to center the window
        x = (screen_width - self.main.width()) // 2
        y = (screen_height - self.main.height()) // 2
        self.main.move(x,y)

        self.main.show()

        
        