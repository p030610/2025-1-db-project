from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
)

class RestaurantDialog(QDialog):
    def __init__(self, parent=None, restaurant_data=None):
        super().__init__(parent)
        self.restaurant_data = restaurant_data
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("음식점 정보")
        layout = QFormLayout()
        
        # 입력 필드 생성
        self.manage_id = QLineEdit()
        self.store_name = QLineEdit()
        self.address = QLineEdit()
        self.legacy_address = QLineEdit()
        
        # 기존 데이터가 있으면 채우기
        if self.restaurant_data:
            self.manage_id.setText(self.restaurant_data[0])
            self.store_name.setText(self.restaurant_data[2])
            self.address.setText(self.restaurant_data[3])
            self.legacy_address.setText(self.restaurant_data[4] if self.restaurant_data[4] else "")
            self.manage_id.setReadOnly(True)  # 관리번호는 수정 불가
        
        # 폼에 위젯 추가
        layout.addRow("관리번호:", self.manage_id)
        layout.addRow("상호명:", self.store_name)
        layout.addRow("주소:", self.address)
        layout.addRow("지번주소:", self.legacy_address)
        
        # 버튼 추가
        button_layout = QHBoxLayout()
        save_button = QPushButton("저장")
        cancel_button = QPushButton("취소")
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            'manage_id': self.manage_id.text(),
            'store_name': self.store_name.text(),
            'address': self.address.text(),
            'legacy_address': self.legacy_address.text()
        } 