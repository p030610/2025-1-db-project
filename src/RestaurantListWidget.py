from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QLabel
)
import psycopg2
from DB_CONFIG import DB_CONFIG

class RestaurantListWidget(QWidget):
    def __init__(self, parent=None, show_actions=True):
        super().__init__(parent)
        self.show_actions = show_actions  # 관리자용 액션 버튼 표시 여부
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 검색 영역
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("음식점명 또는 주소로 검색")
        search_button = QPushButton("검색")
        search_button.clicked.connect(self.search_restaurants)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)
        
        # 버튼 영역 (관리자용)
        if self.show_actions:
            button_layout = QHBoxLayout()
            add_button = QPushButton("음식점 추가")
            edit_button = QPushButton("음식점 수정")
            delete_button = QPushButton("음식점 삭제")
            refresh_button = QPushButton("새로고침")
            
            add_button.clicked.connect(self.add_restaurant)
            edit_button.clicked.connect(self.edit_restaurant)
            delete_button.clicked.connect(self.delete_restaurant)
            refresh_button.clicked.connect(self.refresh_restaurants)
            
            button_layout.addWidget(add_button)
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            button_layout.addWidget(refresh_button)
            layout.addLayout(button_layout)
        
        # 테이블 위젯
        self.restaurant_table = QTableWidget()
        self.restaurant_table.setColumnCount(5)
        self.restaurant_table.setHorizontalHeaderLabels(["관리번호", "허가일자", "상호명", "주소", "지번주소"])
        self.restaurant_table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.restaurant_table)
        
        self.setLayout(layout)
        self.refresh_restaurants()
    
    def refresh_restaurants(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT manage_id, permission_date, store_name, address, legacy_address
                FROM "Restaurant"
                ORDER BY store_name
            """)
            
            restaurants = cursor.fetchall()
            self.restaurant_table.setRowCount(len(restaurants))
            
            for i, restaurant in enumerate(restaurants):
                for j, value in enumerate(restaurant):
                    self.restaurant_table.setItem(i, j, QTableWidgetItem(str(value) if value else ""))
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))
    
    def search_restaurants(self):
        search_text = self.search_input.text().strip()
        if not search_text:
            self.refresh_restaurants()
            return
            
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT manage_id, permission_date, store_name, address, legacy_address
                FROM "Restaurant"
                WHERE store_name ILIKE %s OR address ILIKE %s OR legacy_address ILIKE %s
                ORDER BY store_name
            """, (f'%{search_text}%', f'%{search_text}%', f'%{search_text}%'))
            
            restaurants = cursor.fetchall()
            self.restaurant_table.setRowCount(len(restaurants))
            
            for i, restaurant in enumerate(restaurants):
                for j, value in enumerate(restaurant):
                    self.restaurant_table.setItem(i, j, QTableWidgetItem(str(value) if value else ""))
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))
    
    def get_selected_restaurant(self):
        current_row = self.restaurant_table.currentRow()
        if current_row < 0:
            return None
            
        restaurant_data = []
        for i in range(5):
            item = self.restaurant_table.item(current_row, i)
            restaurant_data.append(item.text() if item else None)
            
        return {
            'manage_id': restaurant_data[0],
            'permission_date': restaurant_data[1],
            'store_name': restaurant_data[2],
            'address': restaurant_data[3],
            'legacy_address': restaurant_data[4]
        }
    
    def on_selection_changed(self):
        # 선택 변경 시 시그널 발생
        self.restaurant_selected.emit(self.get_selected_restaurant())
    
    # 관리자용 메서드들
    def add_restaurant(self):
        from RestaurantDialog import RestaurantDialog
        dialog = RestaurantDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO "Restaurant" (manage_id, store_name, address, legacy_address)
                    VALUES (%s, %s, %s, %s)
                """, (data['manage_id'], data['store_name'], data['address'], data['legacy_address']))
                
                conn.commit()
                conn.close()
                self.refresh_restaurants()
                QMessageBox.information(self, "성공", "음식점이 추가되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))
    
    def edit_restaurant(self):
        current_row = self.restaurant_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "수정할 음식점을 선택하세요.")
            return
        
        restaurant_data = []
        for i in range(5):
            item = self.restaurant_table.item(current_row, i)
            restaurant_data.append(item.text() if item else None)
        
        from RestaurantDialog import RestaurantDialog
        dialog = RestaurantDialog(self, restaurant_data)
        if dialog.exec():
            data = dialog.get_data()
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE "Restaurant"
                    SET store_name = %s, address = %s, legacy_address = %s
                    WHERE manage_id = %s
                """, (data['store_name'], data['address'], data['legacy_address'], data['manage_id']))
                
                conn.commit()
                conn.close()
                self.refresh_restaurants()
                QMessageBox.information(self, "성공", "음식점 정보가 수정되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e))
    
    def delete_restaurant(self):
        current_row = self.restaurant_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 음식점을 선택하세요.")
            return
        
        manage_id = self.restaurant_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(self, "확인", 
                                   "정말로 이 음식점을 삭제하시겠습니까?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM "Restaurant"
                    WHERE manage_id = %s
                """, (manage_id,))
                
                conn.commit()
                conn.close()
                self.refresh_restaurants()
                QMessageBox.information(self, "성공", "음식점이 삭제되었습니다.")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", str(e)) 