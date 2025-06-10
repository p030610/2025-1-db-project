from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel, QLineEdit
)
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import Qt
import psycopg2
from DB_CONFIG import DB_CONFIG

class UserWindow(QMainWindow):
    def __init__(self, user_id, role):
        super().__init__()
        self.setWindowTitle("위생업소 행정처분 관리 시스템-유저 메뉴")
        self.setGeometry(100, 100, 1000, 600)
        self.table=QTableWidget()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_tabs()
        self.user_id=user_id
        self.role=role

    def init_tabs(self):
        self.tabs.addTab(self.view_tab(), "음식점 정보 조회(음식점을 더블클릭해 리뷰를 확인하세요.)")
        self.tabs.addTab(self.review_tab(), "위생평가하기")

    def view_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        refresh_button = QPushButton("새로고침")
        refresh_button.clicked.connect(self.load_data)
        self.load_data()  # Load once on tab creation

        search_input = QLineEdit()
        search_input.setPlaceholderText("검색어 입력 (음식점명)")
        search_input.textChanged.connect(self.filter_table)
        layout.addWidget(QLabel("음식점 정보 조회"))
        
        layout.addWidget(refresh_button)
        layout.addWidget(search_input)
        layout.addWidget(self.table)

        tab.setLayout(layout)   

        return tab
    
    def vie_review_popup(self):
        pass

    def load_data(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT manage_id, store_name, address, permission_date, legacy_name
                FROM "Restaurant"
                ORDER BY permission_date DESC
            """)
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]

            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(["관리 고유번호","점포명","주소","허가일자","기존 점포명"])
            self.table.horizontalHeader().setStretchLastSection(True)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row_idx, col_idx, item)
                    self.table.horizontalHeader().setStretchLastSection(True)
                    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            cursor.close()
            conn.close()
        except Exception as e:
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(["오류"])
            self.table.setItem(0, 0, QTableWidgetItem(str(e)))
    
    def filter_table(self):
        pass

    def review_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("여기에 처분사항 등록 UI가 들어갑니다."))
        tab.setLayout(layout)
        return tab