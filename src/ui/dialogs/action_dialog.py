from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QDateEdit, QLineEdit, QTextEdit, QPushButton
)
from PyQt6.QtCore import QDate

class ActionDialog(QDialog):
    def __init__(self, parent=None, store_id=None, store_name=None):
        super().__init__(parent)
        self.store_id = store_id
        self.store_name = store_name
        self.setWindowTitle("처분내역 추가")
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 식당 정보 표시
        if self.store_name:
            store_label = QLabel(f"식당명: {self.store_name}")
            layout.addWidget(store_label)
        
        # 날짜 입력
        date_layout = QHBoxLayout()
        self.disposal_date = QDateEdit()
        self.disposal_date.setCalendarPopup(True)
        self.disposal_date.setDisplayFormat("yyyy/MM/dd")  # 날짜 표시 형식 변경
        self.disposal_date.setDate(QDate.currentDate())
        
        self.guide_date = QDateEdit()
        self.guide_date.setCalendarPopup(True)
        self.guide_date.setDisplayFormat("yyyy/MM/dd")  # 날짜 표시 형식 변경
        self.guide_date.setDate(QDate.currentDate())
        
        date_layout.addWidget(QLabel("처분일자:"))
        date_layout.addWidget(self.disposal_date)
        date_layout.addWidget(QLabel("지도일자:"))
        date_layout.addWidget(self.guide_date)
        layout.addLayout(date_layout)
        
        # 처분명
        disposal_name_layout = QHBoxLayout()
        disposal_name_layout.addWidget(QLabel("처분명:"))
        self.disposal_name = QLineEdit()
        disposal_name_layout.addWidget(self.disposal_name)
        layout.addLayout(disposal_name_layout)
        
        # 법적근거
        legal_layout = QHBoxLayout()
        legal_layout.addWidget(QLabel("법적근거:"))
        self.legal_reason = QLineEdit()
        legal_layout.addWidget(self.legal_reason)
        layout.addLayout(legal_layout)
        
        # 위반내용
        violation_layout = QVBoxLayout()
        violation_layout.addWidget(QLabel("위반내용:"))
        self.violation = QTextEdit()
        self.violation.setMinimumHeight(150)  # 위반내용 입력 영역 높이 증가
        violation_layout.addWidget(self.violation)
        layout.addLayout(violation_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        save_btn = QPushButton("저장")
        cancel_btn = QPushButton("취소")
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout) 