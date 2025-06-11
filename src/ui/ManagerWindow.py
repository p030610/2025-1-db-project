from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QLabel,
    QLineEdit, QDateEdit, QFormLayout, QDialog, QComboBox, QTextEdit,
    QScrollArea, QFrame, QGridLayout, QGroupBox, QSizePolicy, QHeaderView
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QFont, QPalette, QColor
import psycopg2
from DB_CONFIG import DB_CONFIG
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import platform
from .dialogs.restaurant_dialog import RestaurantDialog, RestaurantDetailDialog

# matplotlib 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:  # Linux
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class ActionDialog(QDialog):
    def __init__(self, parent=None, store_id=None, store_name=None):
        super().__init__(parent)
        self.store_id = store_id
        self.store_name = store_name
        self.setWindowTitle("처분내역 추가")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 식당 정보 표시
        if self.store_name:
            store_label = QLabel(f"식당명: {self.store_name}")
            layout.addWidget(store_label)
        
        # 날짜 입력
        date_layout = QHBoxLayout()
        self.disposal_date = QDateEdit()
        self.disposal_date.setCalendarPopup(True)
        self.disposal_date.setDisplayFormat("yyyy/MM/dd")  # 날짜 표시 형식 변경
        self.disposal_date.setDate(QDate.currentDate())
        
        self.guide_date = QDateEdit()
        self.guide_date.setCalendarPopup(True)
        self.guide_date.setDisplayFormat("yyyy/MM/dd")  # 날짜 표시 형식 변경
        self.guide_date.setDate(QDate.currentDate())
        
        date_layout.addWidget(QLabel("처분일자:"))
        date_layout.addWidget(self.disposal_date)
        date_layout.addWidget(QLabel("지도일자:"))
        date_layout.addWidget(self.guide_date)
        layout.addLayout(date_layout)
        
        # 처분명
        disposal_name_layout = QHBoxLayout()
        disposal_name_layout.addWidget(QLabel("처분명:"))
        self.disposal_name = QLineEdit()
        disposal_name_layout.addWidget(self.disposal_name)
        layout.addLayout(disposal_name_layout)
        
        # 법적근거
        legal_layout = QHBoxLayout()
        legal_layout.addWidget(QLabel("법적근거:"))
        self.legal_reason = QLineEdit()
        legal_layout.addWidget(self.legal_reason)
        layout.addLayout(legal_layout)
        
        # 위반내용
        violation_layout = QVBoxLayout()
        violation_layout.addWidget(QLabel("위반내용:"))
        self.violation = QTextEdit()
        self.violation.setMinimumHeight(150)  # 위반내용 입력 영역 높이 증가
        violation_layout.addWidget(self.violation)
        layout.addLayout(violation_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        save_btn = QPushButton("저장")
        cancel_btn = QPushButton("취소")
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

class RestaurantCard(QWidget):
    def __init__(self, restaurant_data, parent=None):
        super().__init__(parent)
        self.restaurant_data = restaurant_data
        self.setAutoFillBackground(True)  # 배경 자동 채우기 활성화
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#ffffff"))  # 배경색 설정
        self.setPalette(palette)
        self.setFixedSize(300, 150)  # 카드 크기 고정
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 상호명과 주소 표시
        name_label = QLabel(str(self.restaurant_data[1]))  # store_name
        name_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 14px;
            background: transparent;
        """)
        name_label.setWordWrap(True)
        
        address_label = QLabel(str(self.restaurant_data[2]))  # address
        address_label.setStyleSheet("background: transparent;")
        address_label.setWordWrap(True)
        
        # 처분내역 건수와 평균 평점 표시
        action_count = self.restaurant_data[3] if len(self.restaurant_data) > 3 else 0
        avg_rating = self.restaurant_data[4] if len(self.restaurant_data) > 4 else 0
        rating_count = self.restaurant_data[5] if len(self.restaurant_data) > 5 else 0
        
        info_label = QLabel(f"처분내역: {action_count}건 | 평균 평점: {avg_rating}점({rating_count})")
        info_label.setStyleSheet("""
            background: transparent;
            color: #666;
            font-size: 12px;
        """)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 상세보기 버튼
        detail_btn = QPushButton("상세보기")
        detail_btn.clicked.connect(self.show_detail)
        
        # 삭제 버튼
        delete_btn = QPushButton("삭제")
        delete_btn.setStyleSheet("background-color: #ff4444; color: white;")
        delete_btn.clicked.connect(self.delete_restaurant)
        
        button_layout.addWidget(detail_btn)
        button_layout.addWidget(delete_btn)
        
        layout.addWidget(name_label)
        layout.addWidget(address_label)
        layout.addWidget(info_label)
        layout.addLayout(button_layout)
        
        # 카드 자체에만 스타일 적용
        self.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QLabel {
                background: transparent;
            }
        """)
        
        self.setLayout(layout)
        
    def show_detail(self):
        parent = self.parent()
        while parent:
            if isinstance(parent, ManagerWindow):
                parent.show_restaurant_detail(self.restaurant_data[0])  # manage_id
                break
            parent = parent.parent()
            
    def delete_restaurant(self):
        """음식점 삭제"""
        # 확인 대화상자 표시
        reply = QMessageBox.question(
            self,
            "음식점 삭제",
            f"정말로 '{self.restaurant_data[1]}' 음식점을 삭제하시겠습니까?\n\n"
            "이 작업은 되돌릴 수 없으며, 관련된 모든 처분내역과 사용자 평점도 함께 삭제됩니다.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 부모 윈도우에서 cursor 가져오기
                parent = self.parent()
                while parent:
                    if isinstance(parent, ManagerWindow):
                        cursor = parent.cursor
                        break
                    parent = parent.parent()
                
                if cursor:
                    # 트랜잭션 시작
                    cursor.execute("BEGIN")
                    
                    try:
                        # 먼저 관련된 처분내역 삭제
                        cursor.execute("""
                            DELETE FROM "Action"
                            WHERE store_id = %s
                        """, (self.restaurant_data[0],))
                        
                        # 사용자 평점 삭제
                        cursor.execute("""
                            DELETE FROM "UserEvaluation"
                            WHERE store_id = %s
                        """, (self.restaurant_data[0],))
                        
                        # 음식점 삭제
                        cursor.execute("""
                            DELETE FROM "Restaurant"
                            WHERE manage_id = %s
                        """, (self.restaurant_data[0],))
                        
                        # 트랜잭션 커밋
                        cursor.connection.commit()
                        
                        QMessageBox.information(
                            self,
                            "삭제 완료",
                            "음식점이 성공적으로 삭제되었습니다."
                        )
                        
                        # 목록 새로고침
                        parent = self.parent()
                        while parent:
                            if isinstance(parent, ManagerWindow):
                                parent.load_restaurants(reset=True)
                                break
                            parent = parent.parent()
                            
                    except Exception as e:
                        # 오류 발생 시 롤백
                        cursor.connection.rollback()
                        raise e
                        
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "삭제 실패",
                    f"음식점 삭제 중 오류가 발생했습니다:\n{str(e)}"
                )

class RestaurantListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.current_page = 0
        self.has_more = True
        self.is_loading = False
        
    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(10)
        self.setLayout(layout)
        
    def add_restaurant(self, restaurant_data):
        row = self.layout().count() // 3
        col = self.layout().count() % 3
        card = RestaurantCard(restaurant_data, self)
        self.layout().addWidget(card, row, col)
        
    def clear(self):
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.current_page = 0
        self.has_more = True
        self.is_loading = False

class RestaurantDialog(QDialog):
    def __init__(self, parent=None, restaurant_data=None):
        super().__init__(parent)
        self.setWindowTitle("음식점 정보")
        self.setModal(True)
        
        layout = QFormLayout()
        
        self.manage_id = QLineEdit()
        self.permission_date = QDateEdit()
        self.permission_date.setCalendarPopup(True)
        self.permission_date.setDisplayFormat("yyyy/MM/dd")  # 날짜 표시 형식 변경
        self.store_name = QLineEdit()
        self.address = QLineEdit()
        self.legacy_address = QLineEdit()
        
        layout.addRow("관리번호:", self.manage_id)
        layout.addRow("허가일자:", self.permission_date)
        layout.addRow("상호명:", self.store_name)
        layout.addRow("주소:", self.address)
        layout.addRow("지번주소:", self.legacy_address)
        
        buttons = QHBoxLayout()
        self.save_btn = QPushButton("저장")
        self.cancel_btn = QPushButton("취소")
        
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addRow(buttons)
        
        if restaurant_data:
            self.manage_id.setText(restaurant_data[0])
            self.permission_date.setDate(QDate.fromString(restaurant_data[1], "yyyy-MM-dd"))
            self.store_name.setText(restaurant_data[2])
            self.address.setText(restaurant_data[3])
            self.legacy_address.setText(restaurant_data[4])
            self.manage_id.setReadOnly(True)
        
        self.setLayout(layout)

class ManagerWindow(QMainWindow):
    def __init__(self, user_id: int, role: str):
        super().__init__()
        self.setWindowTitle("위생업소 행정처분 관리 시스템-관리자 메뉴")
        self.setGeometry(100, 100, 1200, 800)

        self.user_id = user_id
        self.role = role
        self.search_text = ""
        
        # 데이터베이스 연결
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
        except Exception as e:
            QMessageBox.critical(self, "데이터베이스 연결 오류", str(e))
            return

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_tabs()

    def init_tabs(self):
        self.tabs.addTab(self.create_restaurant_tab(), "음식점 관리")
        self.tabs.addTab(self.create_view_tab(), "처분내역 조회")
        self.tabs.addTab(self.create_stats_tab(), "현황 통계")

    def create_restaurant_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 검색 영역
        search_layout = QHBoxLayout()
        
        # 음식점 추가 버튼
        add_btn = QPushButton("음식점 추가")
        add_btn.clicked.connect(self.add_restaurant)
        search_layout.addWidget(add_btn)
        
        self.restaurant_search_input = QLineEdit()
        self.restaurant_search_input.setObjectName("restaurant_search")
        self.restaurant_search_input.setPlaceholderText("음식점명 또는 주소로 검색")
        self.restaurant_search_input.returnPressed.connect(self.search_restaurants)
        search_btn = QPushButton("검색")
        search_btn.clicked.connect(self.search_restaurants)
        
        search_layout.addWidget(self.restaurant_search_input)
        search_layout.addWidget(search_btn)
        
        # 스크롤 영역
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.verticalScrollBar().valueChanged.connect(self.check_scroll)
        
        # 음식점 목록 위젯
        self.restaurant_list = RestaurantListWidget(self)
        self.scroll.setWidget(self.restaurant_list)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.scroll)
        
        # 초기 데이터 로드
        self.search_text = ""
        self.load_restaurants(reset=True)
        
        tab.setLayout(layout)
        return tab

    def check_scroll(self, value):
        if not self.restaurant_list.has_more or self.restaurant_list.is_loading:
            return
            
        scrollbar = self.scroll.verticalScrollBar()
        if value >= scrollbar.maximum() - 100:  # 스크롤이 끝에서 100픽셀 전에 도달하면
            self.load_more_restaurants()

    def load_restaurants(self, reset=True):
        if reset:
            self.restaurant_list.clear()
            self.restaurant_list.current_page = 0
            self.restaurant_list.has_more = True
        self.load_more_restaurants()

    def load_more_restaurants(self):
        if self.restaurant_list.is_loading or not self.restaurant_list.has_more:
            return
            
        self.restaurant_list.is_loading = True
        page_size = 20
        offset = self.restaurant_list.current_page * page_size
        
        try:
            # 검색어에 따른 쿼리 실행
            if self.search_text:
                self.cursor.execute("""
                    WITH recent_actions AS (
                        SELECT store_id, COUNT(*) as action_count
                        FROM "Action"
                        GROUP BY store_id
                    ),
                    avg_ratings AS (
                        SELECT store_id, 
                               ROUND(AVG(rating)::numeric, 1) as avg_rating,
                               COUNT(*) as rating_count
                        FROM "UserEvaluation"
                        GROUP BY store_id
                    )
                    SELECT r.manage_id, r.store_name, r.address, 
                           COALESCE(ra.action_count, 0) as action_count,
                           COALESCE(ar.avg_rating, 0) as avg_rating,
                           COALESCE(ar.rating_count, 0) as rating_count
                    FROM "Restaurant" r
                    LEFT JOIN recent_actions ra ON r.manage_id = ra.store_id
                    LEFT JOIN avg_ratings ar ON r.manage_id = ar.store_id
                    WHERE r.store_name ILIKE %s OR r.address ILIKE %s
                    ORDER BY r.store_name
                    LIMIT %s OFFSET %s
                """, (f'%{self.search_text}%', f'%{self.search_text}%', page_size, offset))
            else:
                self.cursor.execute("""
                    WITH recent_actions AS (
                        SELECT store_id, COUNT(*) as action_count
                        FROM "Action"
                        GROUP BY store_id
                    ),
                    avg_ratings AS (
                        SELECT store_id, 
                               ROUND(AVG(rating)::numeric, 1) as avg_rating,
                               COUNT(*) as rating_count
                        FROM "UserEvaluation"
                        GROUP BY store_id
                    )
                    SELECT r.manage_id, r.store_name, r.address, 
                           COALESCE(ra.action_count, 0) as action_count,
                           COALESCE(ar.avg_rating, 0) as avg_rating,
                           COALESCE(ar.rating_count, 0) as rating_count
                    FROM "Restaurant" r
                    LEFT JOIN recent_actions ra ON r.manage_id = ra.store_id
                    LEFT JOIN avg_ratings ar ON r.manage_id = ar.store_id
                    ORDER BY r.store_name
                    LIMIT %s OFFSET %s
                """, (page_size, offset))
                
            restaurants = self.cursor.fetchall()
            
            # 결과가 없거나 페이지 크기보다 적으면 더 이상 로드하지 않음
            if len(restaurants) < page_size:
                self.restaurant_list.has_more = False
                
            # 결과 추가
            for restaurant in restaurants:
                self.restaurant_list.add_restaurant(restaurant)
                
            self.restaurant_list.current_page += 1
            
        except Exception as e:
            QMessageBox.critical(self, "데이터 로드 오류", str(e))
        finally:
            self.restaurant_list.is_loading = False

    def search_restaurants(self):
        # 검색어 갱신 및 목록 초기화
        new_search_text = self.restaurant_search_input.text().strip()  # 이름 변경
        print(f"Restaurant search triggered with text: {new_search_text}")  # 디버그 메시지
        if new_search_text != self.search_text:  # 검색어가 변경된 경우에만 리로드
            self.search_text = new_search_text
            self.load_restaurants(reset=True)

    def show_restaurant_detail(self, manage_id):
        try:
            self.cursor.execute("""
                SELECT manage_id, permission_date, store_name, address, legacy_address
                FROM "Restaurant"
                WHERE manage_id = %s
            """, (manage_id,))
            
            restaurant_data = self.cursor.fetchone()
            if restaurant_data:
                dialog = RestaurantDetailDialog(self, restaurant_data, self.cursor)
                if dialog.exec():
                    # 저장된 경우 목록 새로고침
                    self.load_restaurants()
        except Exception as e:
            QMessageBox.critical(self, "데이터 로드 오류", str(e))

    def create_view_tab(self):
        """처분내역 조회 탭 생성"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 검색 영역
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("식당명 또는 주소로 검색")
        self.search_input.textChanged.connect(self.search_actions)  # 검색 메소드 연결
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 처분내역 테이블
        self.action_table = QTableWidget()
        self.action_table.setColumnCount(7)
        self.action_table.setHorizontalHeaderLabels([
            "처분일자", "지도일자", "식당명", "주소", "처분명", "법적근거", "위반내용"
        ])
        
        # 테이블 크기 정책 설정
        self.action_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.action_table.setMinimumHeight(500)
        
        # 헤더 설정
        header = self.action_table.horizontalHeader()
        header.setStretchLastSection(False)
        
        # 컬럼 크기 설정
        column_widths = {
            0: 100,  # 처분일자
            1: 100,  # 지도일자
            2: 150,  # 식당명
            3: 200,  # 주소
            4: 150,  # 처분명
            5: 200,  # 법적근거
            6: 300   # 위반내용
        }
        
        # 각 컬럼의 크기와 정책 설정
        for col, width in column_widths.items():
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
            self.action_table.setColumnWidth(col, width)
        
        # 테이블 설정
        self.action_table.setAlternatingRowColors(True)
        self.action_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.action_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.action_table.verticalHeader().setVisible(False)
        
        # 테이블 스크롤 정책 설정
        self.action_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.action_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        layout.addWidget(self.action_table)
        tab.setLayout(layout)
        
        # 초기 데이터 로드
        self.load_actions()
        
        return tab
        
    def search_actions(self):
        """처분내역 검색"""
        search_text = self.search_input.text().strip()
        self.load_actions(search_text)
        
    def load_actions(self, search_text=None):
        """처분내역 데이터 로드"""
        try:
            # 검색 조건이 있는 경우와 없는 경우를 구분하여 쿼리 실행
            if search_text:
                self.cursor.execute("""
                    SELECT a.disposal_date, a.guide_date, r.store_name, r.address,
                           a.disposal_name, a.legal_reason, a.violation
                    FROM "Action" a
                    JOIN "Restaurant" r ON a.store_id = r.manage_id
                    WHERE r.store_name LIKE %s OR r.address LIKE %s
                    ORDER BY a.disposal_date DESC
                """, (f'%{search_text}%', f'%{search_text}%'))
            else:
                self.cursor.execute("""
                    SELECT a.disposal_date, a.guide_date, r.store_name, r.address,
                           a.disposal_name, a.legal_reason, a.violation
                    FROM "Action" a
                    JOIN "Restaurant" r ON a.store_id = r.manage_id
                    ORDER BY a.disposal_date DESC
                """)
            
            actions = self.cursor.fetchall()
            self.action_table.setRowCount(len(actions))
            
            for i, action in enumerate(actions):
                for j, value in enumerate(action):
                    item = QTableWidgetItem(str(value) if value else "")
                    self.action_table.setItem(i, j, item)
            
        except Exception as e:
            QMessageBox.critical(self, "데이터 로드 오류", str(e))

    def create_stats_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 차트를 위한 Figure 생성
        figure = Figure(figsize=(8, 6))
        
        # 처분내역이 많은 음식점 차트
        ax1 = figure.add_subplot(211)
        self.plot_top_restaurants(ax1)
        
        # 사용자 평점 통계 차트
        ax2 = figure.add_subplot(212)
        self.plot_ratings(ax2)
        
        figure.tight_layout()
        
        # Figure를 Qt 위젯으로 변환
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        
        tab.setLayout(layout)
        return tab

    def plot_top_restaurants(self, ax):
        try:
            self.cursor.execute("""
                SELECT r.store_name, COUNT(*) as action_count
                FROM "Action" a
                JOIN "Restaurant" r ON a.store_id = r.manage_id
                GROUP BY r.manage_id, r.store_name
                ORDER BY action_count DESC
                LIMIT 10
            """)
            data = self.cursor.fetchall()
            
            stores = [row[0] for row in data]
            counts = [row[1] for row in data]
            
            ax.bar(stores, counts)
            ax.set_title("처분내역이 많은 상위 10개 음식점")
            ax.set_xlabel("음식점")
            ax.set_ylabel("처분내역 수")
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        except Exception as e:
            QMessageBox.critical(self, "차트 생성 오류", str(e))

    def plot_ratings(self, ax):
        try:
            self.cursor.execute("""
                SELECT rating, COUNT(*) as rating_count
                FROM "UserEvaluation"
                GROUP BY rating
                ORDER BY rating
            """)
            data = self.cursor.fetchall()
            
            ratings = [row[0] for row in data]
            counts = [row[1] for row in data]
            
            ax.bar(ratings, counts)
            ax.set_title("사용자 평점 분포")
            ax.set_xlabel("평점")
            ax.set_ylabel("평가 수")
            ax.set_xticks(range(1, 6))
            
        except Exception as e:
            QMessageBox.critical(self, "차트 생성 오류", str(e))

    def add_restaurant(self):
        """음식점 추가"""
        dialog = RestaurantDialog(self)
        if dialog.exec():
            try:
                # 필수 필드 검증
                if not dialog.manage_id.text().strip():
                    raise ValueError("관리번호는 필수 입력 항목입니다.")
                if not dialog.store_name.text().strip():
                    raise ValueError("상호명은 필수 입력 항목입니다.")
                if not dialog.address.text().strip():
                    raise ValueError("주소는 필수 입력 항목입니다.")
                
                # 중복 관리번호 검사
                self.cursor.execute("""
                    SELECT COUNT(*) FROM "Restaurant"
                    WHERE manage_id = %s
                """, (dialog.manage_id.text().strip(),))
                
                if self.cursor.fetchone()[0] > 0:
                    raise ValueError("이미 존재하는 관리번호입니다.")
                
                # 음식점 추가
                self.cursor.execute("""
                    INSERT INTO "Restaurant" (
                        manage_id, permission_date, store_name,
                        address, legacy_address
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    dialog.manage_id.text().strip(),
                    dialog.permission_date.date().toString("yyyy-MM-dd"),
                    dialog.store_name.text().strip(),
                    dialog.address.text().strip(),
                    dialog.legacy_address.text().strip()
                ))
                
                self.cursor.connection.commit()
                QMessageBox.information(self, "성공", "음식점이 추가되었습니다.")
                self.load_restaurants(reset=True)
                
            except ValueError as e:
                QMessageBox.warning(self, "입력 오류", str(e))
            except Exception as e:
                self.cursor.connection.rollback()
                QMessageBox.critical(self, "추가 실패", str(e))

    def closeEvent(self, event):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass
        event.accept()