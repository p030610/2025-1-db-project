from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel, QLineEdit, QMenu
)
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import Qt, QPoint
import psycopg2
from DB_CONFIG import DB_CONFIG
from ui.ActionList import ActionList
from ui.EvaluationForm import EvaluationForm
from ui.ReviewList import ReviewList

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


        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def init_tabs(self):
        self.tabs.addTab(self.view_tab(), "음식점 정보")

    def view_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # refresh_button = QPushButton("새로고침")
        # refresh_button.clicked.connect(self.load_data)
        self.load_data()  # Load once on tab creation

        search_input = QLineEdit()
        search_input.setPlaceholderText("검색어 입력 (음식점명)")
        search_input.textChanged.connect(self.filter_table)
        # layout.addWidget(QLabel("음식점 정보 조회"))
        
        layout.addWidget(search_input)
        # layout.addWidget(refresh_button)
        layout.addWidget(self.table)
        tab.setLayout(layout)   

        return tab

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
            self.table.setHorizontalHeaderLabels(["관리 고유번호","점포명","도로명 주소","허가일자","지번 주소"])
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
        search_text = self.sender().text().lower()  # Case-insensitive search

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # Column 1 = store_name
            if item:
                store_name = item.text().lower()
                match = search_text in store_name
                self.table.setRowHidden(row, not match)

    def show_context_menu(self, pos: QPoint):
        # Get global position
        global_pos = self.table.viewport().mapToGlobal(pos)

        # Get clicked row
        item = self.table.itemAt(pos)
        if item is None:
            return  # Clicked outside any cell

        row = item.row()

        # Create popup menu
        menu = QMenu(self)

        action_review = menu.addAction("새 리뷰 작성")
        action_detail = menu.addAction("처분내역 열람")
        action_view_review=menu.addAction("작성된 리뷰 열람")

        action = menu.exec(global_pos)

        # Handle menu selection
        storeid=self.table.item(row,0).text()
        storename=self.table.item(row,1).text()
        if action == action_review:
            self.eval_form = EvaluationForm(self.user_id, storeid)
            self.eval_form.show()

        elif action == action_detail:
            self.actionlist = ActionList(storename, storeid)
            self.actionlist.show()
        elif action == action_view_review:
            self.review_list = ReviewList(storename, storeid)
            self.review_list.show()
