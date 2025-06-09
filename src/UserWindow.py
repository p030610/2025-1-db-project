from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel
)
import DatabaseManager
import psycopg2
from DB_CONFIG import DB_CONFIG
from RestaurantListWidget import RestaurantListWidget

class UserWindow(QMainWindow):
    def __init__(self, user_id, role):
        super().__init__()
        self.user_id = user_id
        self.role = role
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("위생업소 행정처분 관리 시스템 - 일반 사용자 메뉴")
        self.setGeometry(100, 100, 1200, 800)
        
        # 탭 위젯 생성
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 탭 추가
        self.tabs.addTab(self.create_restaurant_tab(), "음식점 조회")
        self.tabs.addTab(self.create_disposal_tab(), "처분내역 조회")
    
    def create_restaurant_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 음식점 목록 위젯 추가 (관리자용 액션 버튼 숨김)
        self.restaurant_list = RestaurantListWidget(self, show_actions=False)
        self.restaurant_list.restaurant_selected.connect(self.on_restaurant_selected)
        layout.addWidget(self.restaurant_list)
        
        tab.setLayout(layout)
        return tab
    
    def create_disposal_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 음식점 목록 위젯 추가 (관리자용 액션 버튼 숨김)
        self.disposal_restaurant_list = RestaurantListWidget(self, show_actions=False)
        self.disposal_restaurant_list.restaurant_selected.connect(self.on_disposal_restaurant_selected)
        layout.addWidget(self.disposal_restaurant_list)
        
        # 처분내역 테이블
        self.disposal_table = QTableWidget()
        self.disposal_table.setColumnCount(7)
        self.disposal_table.setHorizontalHeaderLabels([
            "처분ID", "처분일자", "음식점ID", "안내일자", 
            "처분명칭", "법적사유", "위반내용"
        ])
        layout.addWidget(self.disposal_table)
        
        tab.setLayout(layout)
        return tab
    
    def on_restaurant_selected(self, restaurant):
        if restaurant:
            # 음식점이 선택되었을 때의 동작
            pass
    
    def on_disposal_restaurant_selected(self, restaurant):
        if restaurant:
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT action_id, disposal_date, store_id, guide_date,
                           disposal_name, legal_reason, violation
                    FROM "Action"
                    WHERE store_id = %s
                    ORDER BY disposal_date DESC
                """, (restaurant['manage_id'],))
                
                disposals = cursor.fetchall()
                self.disposal_table.setRowCount(len(disposals))
                
                for i, disposal in enumerate(disposals):
                    for j, value in enumerate(disposal):
                        self.disposal_table.setItem(i, j, QTableWidgetItem(str(value) if value else ""))
                
                conn.close()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))


