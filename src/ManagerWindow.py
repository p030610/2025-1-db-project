from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, 
    QLabel, QLineEdit, QFormLayout, QDialog, QComboBox
)
import psycopg2
from DB_CONFIG import DB_CONFIG
from Disposalform import DisposalForm
from RestaurantListWidget import RestaurantListWidget

class RestaurantDialog(QDialog):
    def __init__(self, parent=None, restaurant_data=None):
        super().__init__(parent)
        self.restaurant_data = restaurant_data
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("음식점 정보")
        layout = QFormLayout()
        
        # 입력 필드 생성
        self.manage_id = QLineEdit()
        self.store_name = QLineEdit()
        self.address = QLineEdit()
        self.legacy_address = QLineEdit()
        
        # 기존 데이터가 있으면 채우기
        if self.restaurant_data:
            self.manage_id.setText(self.restaurant_data[0])
            self.store_name.setText(self.restaurant_data[2])
            self.address.setText(self.restaurant_data[3])
            self.legacy_address.setText(self.restaurant_data[4] if self.restaurant_data[4] else "")
            self.manage_id.setReadOnly(True)  # 관리번호는 수정 불가
        
        # 폼에 위젯 추가
        layout.addRow("관리번호:", self.manage_id)
        layout.addRow("상호명:", self.store_name)
        layout.addRow("주소:", self.address)
        layout.addRow("지번주소:", self.legacy_address)
        
        # 버튼 추가
        button_layout = QHBoxLayout()
        save_button = QPushButton("저장")
        cancel_button = QPushButton("취소")
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            'manage_id': self.manage_id.text(),
            'store_name': self.store_name.text(),
            'address': self.address.text(),
            'legacy_address': self.legacy_address.text()
        }

class UserDialog(QDialog):
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("사용자 정보")
        layout = QFormLayout()
        
        # 입력 필드 생성
        self.username = QLineEdit()
        self.role = QComboBox()
        self.role.addItems(['user', 'admin'])
        
        # 기존 데이터가 있으면 채우기
        if self.user_data:
            self.username.setText(self.user_data[1])
            self.role.setCurrentText(self.user_data[2])
            self.username.setReadOnly(True)  # 사용자명은 수정 불가
        
        # 폼에 위젯 추가
        layout.addRow("사용자명:", self.username)
        layout.addRow("역할:", self.role)
        
        # 버튼 추가
        button_layout = QHBoxLayout()
        save_button = QPushButton("저장")
        cancel_button = QPushButton("취소")
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            'username': self.username.text(),
            'role': self.role.currentText()
        }

class ManagerWindow(QMainWindow):
    def __init__(self, user_id, role):
        super().__init__()
        self.user_id = user_id
        self.role = role
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("위생업소 행정처분 관리 시스템 - 관리자 메뉴")
        self.setGeometry(100, 100, 1200, 800)
        
        # 탭 위젯 생성
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 탭 추가
        self.tabs.addTab(self.create_restaurant_tab(), "음식점 관리")
        self.tabs.addTab(self.create_disposal_tab(), "행정처분 관리")
        self.tabs.addTab(self.create_user_tab(), "사용자 관리")
    
    def create_restaurant_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 음식점 목록 위젯 추가 (관리자용 액션 버튼 표시)
        self.restaurant_list = RestaurantListWidget(self, show_actions=True)
        layout.addWidget(self.restaurant_list)
        
        tab.setLayout(layout)
        return tab
    
    def create_disposal_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        add_button = QPushButton("처분사항 추가")
        edit_button = QPushButton("처분사항 수정")
        delete_button = QPushButton("처분사항 삭제")
        refresh_button = QPushButton("새로고침")
        
        add_button.clicked.connect(self.add_disposal)
        edit_button.clicked.connect(self.edit_disposal)
        delete_button.clicked.connect(self.delete_disposal)
        refresh_button.clicked.connect(self.refresh_disposals)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)
        
        # 테이블 위젯
        self.disposal_table = QTableWidget()
        self.disposal_table.setColumnCount(7)
        self.disposal_table.setHorizontalHeaderLabels([
            "처분ID", "처분일자", "음식점ID", "안내일자", 
            "처분명칭", "법적사유", "위반내용"
        ])
        layout.addWidget(self.disposal_table)
        
        tab.setLayout(layout)
        self.refresh_disposals()
        return tab
    
    def create_user_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        add_button = QPushButton("사용자 추가")
        edit_button = QPushButton("사용자 수정")
        delete_button = QPushButton("사용자 삭제")
        refresh_button = QPushButton("새로고침")
        
        add_button.clicked.connect(self.add_user)
        edit_button.clicked.connect(self.edit_user)
        delete_button.clicked.connect(self.delete_user)
        refresh_button.clicked.connect(self.refresh_users)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)
        
        # 테이블 위젯
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "사용자명", "역할", "가입일"])
        layout.addWidget(self.user_table)
        
        tab.setLayout(layout)
        self.refresh_users()
        return tab
    
    def refresh_disposals(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT action_id, disposal_date, store_id, guide_date,
                       disposal_name, legal_reason, violation
                FROM "Action"
                ORDER BY disposal_date DESC
            """)
            
            disposals = cursor.fetchall()
            self.disposal_table.setRowCount(len(disposals))
            
            for i, disposal in enumerate(disposals):
                for j, value in enumerate(disposal):
                    self.disposal_table.setItem(i, j, QTableWidgetItem(str(value) if value else ""))
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))
    
    def refresh_users(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, username, role, reg_date
                FROM "User"
                ORDER BY user_id
            """)
            
            users = cursor.fetchall()
            self.user_table.setRowCount(len(users))
            
            for i, user in enumerate(users):
                for j, value in enumerate(user):
                    self.user_table.setItem(i, j, QTableWidgetItem(str(value) if value else ""))
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))
    
    def add_disposal(self):
        form = DisposalForm()
        if form.exec():
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO "Action" (disposal_date, store_id, guide_date,
                                        disposal_name, legal_reason, violation)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (form.disposal_date_input.date().toPyDate(),
                      form.store_id_input.text(),
                      form.guide_date_input.date().toPyDate(),
                      form.disposal_name_input.text(),
                      form.legal_reason_input.text(),
                      form.violation_input.toPlainText()))
                
                conn.commit()
                conn.close()
                self.refresh_disposals()
                QMessageBox.information(self, "성공", "처분사항이 추가되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))
    
    def edit_disposal(self):
        current_row = self.disposal_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "수정할 처분사항을 선택하세요.")
            return
        
        # TODO: 처분사항 수정 기능 구현
        QMessageBox.information(self, "알림", "처분사항 수정 기능은 아직 구현되지 않았습니다.")
    
    def delete_disposal(self):
        current_row = self.disposal_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 처분사항을 선택하세요.")
            return
        
        action_id = self.disposal_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(self, "확인", 
                                   "정말로 이 처분사항을 삭제하시겠습니까?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM "Action"
                    WHERE action_id = %s
                """, (action_id,))
                
                conn.commit()
                conn.close()
                self.refresh_disposals()
                QMessageBox.information(self, "성공", "처분사항이 삭제되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))
    
    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO "User" (username, role)
                    VALUES (%s, %s)
                """, (data['username'], data['role']))
                
                conn.commit()
                conn.close()
                self.refresh_users()
                QMessageBox.information(self, "성공", "사용자가 추가되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))
    
    def edit_user(self):
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "수정할 사용자를 선택하세요.")
            return
        
        user_data = []
        for i in range(4):
            item = self.user_table.item(current_row, i)
            user_data.append(item.text() if item else None)
        
        dialog = UserDialog(self, user_data)
        if dialog.exec():
            data = dialog.get_data()
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE "User"
                    SET role = %s
                    WHERE username = %s
                """, (data['role'], data['username']))
                
                conn.commit()
                conn.close()
                self.refresh_users()
                QMessageBox.information(self, "성공", "사용자 정보가 수정되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))
    
    def delete_user(self):
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 사용자를 선택하세요.")
            return
        
        user_id = self.user_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(self, "확인", 
                                   "정말로 이 사용자를 삭제하시겠습니까?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM "User"
                    WHERE user_id = %s
                """, (user_id,))
                
                conn.commit()
                conn.close()
                self.refresh_users()
                QMessageBox.information(self, "성공", "사용자가 삭제되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))