from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget)
from PyQt6.QtCore import Qt
import psycopg2
import bcrypt
from DB_CONFIG import DB_CONFIG
from UserWindow import UserWindow
from ManagerWindow import ManagerWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('위생업소 행정처분 관리 시스템 - 로그인')
        self.setFixedSize(400, 300)
        
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 스택 위젯 생성 (로그인/회원가입 화면 전환용)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # 로그인 화면
        login_widget = QWidget()
        login_layout = QVBoxLayout(login_widget)
        
        # 로그인 폼
        login_form = QWidget()
        form_layout = QVBoxLayout(login_form)
        
        # 사용자명 입력
        username_layout = QHBoxLayout()
        username_label = QLabel('아이디:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('아이디를 입력하세요')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)
        
        # 비밀번호 입력
        password_layout = QHBoxLayout()
        password_label = QLabel('비밀번호:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText('비밀번호를 입력하세요')
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)
        
        login_layout.addWidget(login_form)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        login_button = QPushButton('로그인')
        register_button = QPushButton('회원가입')
        login_button.clicked.connect(self.login)
        register_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)
        login_layout.addLayout(button_layout)
        
        # 회원가입 화면
        register_widget = QWidget()
        register_layout = QVBoxLayout(register_widget)
        
        # 회원가입 폼
        register_form = QWidget()
        reg_form_layout = QVBoxLayout(register_form)
        
        # 사용자명 입력
        reg_username_layout = QHBoxLayout()
        reg_username_label = QLabel('아이디:')
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText('아이디를 입력하세요')
        reg_username_layout.addWidget(reg_username_label)
        reg_username_layout.addWidget(self.reg_username_input)
        reg_form_layout.addLayout(reg_username_layout)
        
        # 비밀번호 입력
        reg_password_layout = QHBoxLayout()
        reg_password_label = QLabel('비밀번호:')
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password_input.setPlaceholderText('비밀번호를 입력하세요')
        reg_password_layout.addWidget(reg_password_label)
        reg_password_layout.addWidget(self.reg_password_input)
        reg_form_layout.addLayout(reg_password_layout)
        
        # 비밀번호 확인
        reg_confirm_layout = QHBoxLayout()
        reg_confirm_label = QLabel('비밀번호 확인:')
        self.reg_confirm_input = QLineEdit()
        self.reg_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_confirm_input.setPlaceholderText('비밀번호를 다시 입력하세요')
        reg_confirm_layout.addWidget(reg_confirm_label)
        reg_confirm_layout.addWidget(self.reg_confirm_input)
        reg_form_layout.addLayout(reg_confirm_layout)
        
        register_layout.addWidget(register_form)
        
        # 버튼 영역
        reg_button_layout = QHBoxLayout()
        submit_button = QPushButton('가입하기')
        back_button = QPushButton('뒤로가기')
        submit_button.clicked.connect(self.register)
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        reg_button_layout.addWidget(submit_button)
        reg_button_layout.addWidget(back_button)
        register_layout.addLayout(reg_button_layout)
        
        # 스택에 위젯 추가
        self.stack.addWidget(login_widget)
        self.stack.addWidget(register_widget)
    
    def hash_password(self, password):
        """비밀번호를 해시화하는 함수"""
        # bcrypt로 해시화 (바이트 문자열 반환)
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # UTF-8 문자열로 변환하여 반환
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed):
        """해시화된 비밀번호를 검증하는 함수"""
        # 해시화된 비밀번호를 바이트로 변환하여 검증
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, '오류', '모든 필드를 입력해주세요.')
            return
        
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # 사용자 정보 조회
            cursor.execute("""
                SELECT user_id, role, password_hash FROM "User"
                WHERE username = %s
            """, (username,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and self.verify_password(password, result[2]):
                user_id, role = result[0], result[1]
                role_text = "관리자" if role == "admin" else "일반 사용자"
                QMessageBox.information(self, "성공", f"{role_text} 로그인 성공")
                self.open_main_window(user_id, role)
            else:
                QMessageBox.warning(self, "실패", "아이디 또는 비밀번호가 틀렸습니다.")
                
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))
    
    def register(self):
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()
        confirm = self.reg_confirm_input.text()
        
        if not username or not password or not confirm:
            QMessageBox.warning(self, '오류', '모든 필드를 입력해주세요.')
            return
        
        if password != confirm:
            QMessageBox.warning(self, '오류', '비밀번호가 일치하지 않습니다.')
            return
        
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # 사용자명 중복 체크
            cursor.execute("SELECT username FROM \"User\" WHERE username = %s", (username,))
            if cursor.fetchone():
                QMessageBox.warning(self, '오류', '이미 존재하는 아이디입니다.')
                return
            
            # 비밀번호 해시화 (이미 UTF-8 문자열로 반환됨)
            hashed_password = self.hash_password(password)
            
            # 새 사용자 등록
            cursor.execute("""
                INSERT INTO "User" (username, password_hash, role)
                VALUES (%s, %s, 'user')
            """, (username, hashed_password))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, '성공', '회원가입이 완료되었습니다.')
            self.stack.setCurrentIndex(0)  # 로그인 화면으로 전환
            self.reg_username_input.clear()
            self.reg_password_input.clear()
            self.reg_confirm_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))
    
    def open_main_window(self, user_id, role):
        if role == "admin":
            self.main = ManagerWindow(user_id, role)
        else:
            self.main = UserWindow(user_id, role)
        self.main.show()
        self.close()
