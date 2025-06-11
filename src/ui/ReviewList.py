import sys
import psycopg2
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QApplication, QMessageBox
)
from DB_CONFIG import DB_CONFIG
from PyQt6.QtCore import Qt

class ReviewList(QWidget):
    def __init__(self, store_name, store_id):
        super().__init__()
        self.setWindowTitle(f"{store_name} - 사용자 리뷰")
        self.resize(800, 400)
        self.store_id = store_id

        self.layout = QVBoxLayout()
        self.label = QLabel(f"<b>{store_name}</b>에 대한 사용자 리뷰")
        self.table = QTableWidget()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.load_reviews()

    def load_reviews(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT rating, comment, photo_url, eval_date, status
                FROM "UserEvaluation"
                WHERE store_id = %s
                ORDER BY eval_date DESC
            """, (self.store_id,))
            rows = cursor.fetchall()

            headers = ["평점", "코멘트", "사진 URL", "작성일시", "상태"]
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
            QMessageBox.critical(self, "Error", f"리뷰를 불러오는 중 오류 발생:\n{str(e)}")
