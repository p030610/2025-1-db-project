from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel
)
import DatabaseManager

class UserWindow(QMainWindow):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.setWindowTitle("위생업소 행정처분 관리 시스템-유저 메뉴")
        self.setGeometry(100, 100, 1000, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_tabs()
        self.db=db

    def init_tabs(self):
        self.tabs.addTab(self.create_view_tab(), "음식점 정보 조회")
        self.tabs.addTab(self.create_create_tab(), "위생평가")

    def create_view_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("여기에 처분내역 조회 UI가 들어갑니다."))
        tab.setLayout(layout)
        return tab

    def create_create_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("여기에 처분사항 등록 UI가 들어갑니다."))
        tab.setLayout(layout)
        return tab

    def create_stats_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("여기에 통계 및 차트가 들어갑니다."))
        tab.setLayout(layout)
        return tab


