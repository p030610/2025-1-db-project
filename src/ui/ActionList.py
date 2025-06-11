import sys
import psycopg2
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QApplication, QMessageBox
)
from DB_CONFIG import DB_CONFIG
from PyQt6.QtCore import Qt


class ActionList(QWidget):
    def __init__(self, store_name, store_id):
        super().__init__()
        self.setWindowTitle(f"{store_name} - 행정처분 내역")
        self.resize(800, 400)
        self.store_id = store_id

        self.layout = QVBoxLayout()
        self.label = QLabel(f"<b>{store_name}</b>의 행정처분 내역")
        self.table = QTableWidget()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.load_actions()

    def load_actions(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            print(self.store_id)
            cursor.execute("""
                SELECT disposal_date, guide_date, disposal_name,
                       legal_reason, violation
                FROM "Action"
                WHERE store_id = %s
                ORDER BY disposal_date DESC
            """, (self.store_id,))
            rows = cursor.fetchall()

            headers = ["처분일자", "안내일자", "처분명", "법적근거", "위반내용"]
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.horizontalHeader().setStretchLastSection(True)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for row_idx, row_data in enumerate(rows):
                for col_idx, cell in enumerate(row_data):
                    item = QTableWidgetItem(str(cell) if cell else "")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row_idx, col_idx, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"데이터 불러오기 실패: {str(e)}")
