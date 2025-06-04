from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.setWindowTitle("Restaurant Inspection System (PostgreSQL)")
        self.setGeometry(100, 100, 1000, 600)

        self.db = db
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.table_names = ["User", "Restaurant", "UserEvaluation", "Action"]
        self.init_tabs()

    def init_tabs(self):
        for table in self.table_names:
            tab = QWidget()
            layout = QVBoxLayout()

            table_widget = QTableWidget()
            layout.addWidget(table_widget)

            btn_layout = QHBoxLayout()
            add_btn = QPushButton("Add")
            edit_btn = QPushButton("Edit")
            del_btn = QPushButton("Delete")
            btn_layout.addWidget(add_btn)
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            layout.addLayout(btn_layout)

            tab.setLayout(layout)
            self.tabs.addTab(tab, table)

            self.populate_table(table_widget, table)

    def populate_table(self, widget: QTableWidget, table_name: str):
        columns, rows = self.db.fetch_all(table_name)
        widget.setColumnCount(len(columns))
        widget.setRowCount(len(rows))
        widget.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                widget.setItem(row_idx, col_idx, item)