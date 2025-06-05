from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel, QFormLayout, QLineEdit, QTextEdit, QDateEdit
)
from PyQt6.QtCore import *

class DisposalForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        self.store_id_input = QLineEdit()
        self.disposal_date_input = QDateEdit()
        self.disposal_date_input.setCalendarPopup(True)
        self.disposal_date_input.setDate(QDate.currentDate())

        self.disposal_name_input = QLineEdit()
        self.legal_reason_input = QLineEdit()
        self.violation_input = QTextEdit()

        self.submit_btn = QPushButton("처분사항 등록")
        self.submit_btn.clicked.connect(self.save_to_db)

        layout.addRow("음식점 관리번호 (store_id):", self.store_id_input)
        layout.addRow("처분 날짜:", self.disposal_date_input)
        layout.addRow("처분 명칭:", self.disposal_name_input)
        layout.addRow("법적 사유:", self.legal_reason_input)
        layout.addRow("위반 내용:", self.violation_input)
        layout.addRow(self.submit_btn)

        self.setLayout(layout)