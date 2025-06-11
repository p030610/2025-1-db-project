from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QDateEdit, QPushButton, QFormLayout,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QGroupBox, QSizePolicy, QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from .action_dialog import ActionDialog

class RestaurantDialog(QDialog):
    def __init__(self, parent=None, restaurant_data=None):
        super().__init__(parent)
        self.setWindowTitle("음식점 정보")
        self.setModal(True)
        
        layout = QFormLayout()
        
        self.manage_id = QLineEdit()
        self.permission_date = QDateEdit()
        self.permission_date.setCalendarPopup(True)
        self.permission_date.setDisplayFormat("yyyy/MM/dd")  # 날짜 표시 형식 변경
        self.store_name = QLineEdit()
        self.address = QLineEdit()
        self.legacy_address = QLineEdit()
        
        layout.addRow("관리번호:", self.manage_id)
        layout.addRow("허가일자:", self.permission_date)
        layout.addRow("상호명:", self.store_name)
        layout.addRow("주소:", self.address)
        layout.addRow("지번주소:", self.legacy_address)
        
        buttons = QHBoxLayout()
        self.save_btn = QPushButton("저장")
        self.cancel_btn = QPushButton("취소")
        
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addRow(buttons)
        
        if restaurant_data:
            self.manage_id.setText(restaurant_data[0])
            self.permission_date.setDate(QDate.fromString(restaurant_data[1], "yyyy-MM-dd"))
            self.store_name.setText(restaurant_data[2])
            self.address.setText(restaurant_data[3])
            self.legacy_address.setText(restaurant_data[4])
            self.manage_id.setReadOnly(True)
        
        self.setLayout(layout)

class RestaurantDetailDialog(QDialog):
    def __init__(self, parent=None, restaurant_data=None, cursor=None):
        super().__init__(parent)
        self.setWindowTitle("음식점 상세 정보")
        self.setModal(True)
        self.cursor = cursor
        
        # 다이얼로그 크기 설정
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # 기본 정보 표시
        info_group = QGroupBox("기본 정보")
        info_layout = QFormLayout()
        info_layout.setSpacing(10)
        
        self.manage_id = QLineEdit()
        self.permission_date = QDateEdit()
        self.permission_date.setCalendarPopup(True)
        self.permission_date.setDisplayFormat("yyyy/MM/dd")  # 날짜 표시 형식 변경
        self.store_name = QLineEdit()
        self.address = QLineEdit()
        self.legacy_address = QLineEdit()
        
        # 입력 필드 크기 설정
        for field in [self.manage_id, self.store_name, self.address, self.legacy_address]:
            field.setMinimumWidth(400)
        
        info_layout.addRow("관리번호:", self.manage_id)
        info_layout.addRow("허가일자:", self.permission_date)
        info_layout.addRow("상호명:", self.store_name)
        info_layout.addRow("주소:", self.address)
        info_layout.addRow("지번주소:", self.legacy_address)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 처분내역 테이블
        action_group = QGroupBox("처분내역")
        action_layout = QVBoxLayout()
        
        self.action_table = QTableWidget()
        self.action_table.setColumnCount(5)
        self.action_table.setHorizontalHeaderLabels([
            "처분일자", "지도일자", "처분명", "법적근거", "위반내용"
        ])
        
        # 테이블 크기 정책 설정
        self.action_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.action_table.setMinimumHeight(500)
        
        # 헤더 설정
        header = self.action_table.horizontalHeader()
        header.setStretchLastSection(False)
        
        # 컬럼 크기 설정
        column_widths = {
            0: 100,  # 처분일자
            1: 100,  # 지도일자
            2: 150,  # 처분명
            3: 250,  # 법적근거
            4: 300   # 위반내용
        }
        
        # 각 컬럼의 크기와 정책 설정
        for col, width in column_widths.items():
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
            self.action_table.setColumnWidth(col, width)
        
        # 테이블 설정
        self.action_table.setAlternatingRowColors(True)
        self.action_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.action_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.action_table.verticalHeader().setVisible(False)
        
        # 테이블 스크롤 정책 설정
        self.action_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.action_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        action_layout.addWidget(self.action_table)
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        self.add_action_btn = QPushButton("처분내역 추가")
        self.save_btn = QPushButton("저장")
        self.cancel_btn = QPushButton("취소")
        
        self.add_action_btn.clicked.connect(self.add_action)
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.add_action_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # 데이터 설정
        if restaurant_data:
            self.manage_id.setText(restaurant_data[0])
            try:
                if isinstance(restaurant_data[1], str):
                    date = QDate.fromString(restaurant_data[1], "yyyy-MM-dd")
                else:
                    date = QDate(restaurant_data[1].year, restaurant_data[1].month, restaurant_data[1].day)
                self.permission_date.setDate(date)
            except:
                self.permission_date.setDate(QDate.currentDate())
                
            self.store_name.setText(restaurant_data[2])
            self.address.setText(restaurant_data[3])
            self.legacy_address.setText(restaurant_data[4])
            self.manage_id.setReadOnly(True)
            self.load_actions()
        
        self.setLayout(layout)
    
    def load_actions(self):
        try:
            self.cursor.execute("""
                SELECT disposal_date, guide_date, disposal_name, legal_reason, violation
                FROM "Action"
                WHERE store_id = %s
                ORDER BY disposal_date DESC
            """, (self.manage_id.text(),))
            
            actions = self.cursor.fetchall()
            self.action_table.setRowCount(len(actions))
            for i, action in enumerate(actions):
                for j, value in enumerate(action):
                    if j < 2 and value:  # 날짜 필드 처리
                        if isinstance(value, str):
                            item = QTableWidgetItem(value)
                        else:
                            item = QTableWidgetItem(value.strftime("%Y-%m-%d"))
                    else:
                        item = QTableWidgetItem(str(value) if value else "")
                    self.action_table.setItem(i, j, item)
        except Exception as e:
            QMessageBox.critical(self, "데이터 로드 오류", str(e))
    
    def add_action(self):
        dialog = ActionDialog(self, self.manage_id.text(), self.store_name.text())
        if dialog.exec():
            try:
                self.cursor.execute("""
                    INSERT INTO "Action" (
                        disposal_date, store_id, guide_date,
                        disposal_name, legal_reason, violation
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    dialog.disposal_date.date().toString("yyyy-MM-dd"),
                    dialog.store_id,
                    dialog.guide_date.date().toString("yyyy-MM-dd"),
                    dialog.disposal_name.text(),
                    dialog.legal_reason.text(),
                    dialog.violation.toPlainText()
                ))
                self.cursor.connection.commit()
                self.load_actions()
                QMessageBox.information(self, "성공", "처분내역이 추가되었습니다.")
            except Exception as e:
                self.cursor.connection.rollback()
                QMessageBox.critical(self, "추가 실패", str(e)) 