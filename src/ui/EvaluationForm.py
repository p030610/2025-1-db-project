import sys
import psycopg2
from DB_CONFIG import DB_CONFIG
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox,
    QPushButton, QFormLayout, QMessageBox
)

class EvaluationForm(QWidget):
    def __init__(self, user_id, store_id):
        super().__init__()
        self.setWindowTitle("평가하기")
        self.resize(400, 300)

        # Store internal IDs
        self.user_id = user_id
        self.store_id = store_id

        # Create form layout
        layout = QFormLayout()

        # Fields
        self.rating_input = QComboBox()
        self.rating_input.addItems([str(i) for i in range(1, 6)])
        self.comment_input = QTextEdit()
        self.photo_url_input = QLineEdit()
        self.status_input = QLineEdit()

        self.submit_btn = QPushButton("평가하기")
        self.submit_btn.clicked.connect(self.submit_evaluation)

        # Add widgets to form
        layout.addRow("평점:", self.rating_input)
        layout.addRow("비고:", self.comment_input)
        layout.addRow("사진 URL (필수사항 아님):", self.photo_url_input)
        layout.addRow("상태:", self.status_input)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def submit_evaluation(self):
        rating = int(self.rating_input.currentText())
        comment = self.comment_input.toPlainText()
        photo_url = self.photo_url_input.text()
        status = self.status_input.text()

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO "UserEvaluation" (store_id, user_id, rating, comment, photo_url, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.store_id, self.user_id, rating, comment, photo_url, status))

            conn.commit()
            cur.close()
            conn.close()

            QMessageBox.information(self, "성공!!", "리뷰가 저장되었습니다.")

            # Clear form
            self.comment_input.clear()
            self.photo_url_input.clear()
            self.status_input.clear()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.close()


if __name__ == "__main__":
    # Simulate logged-in user and selected store
    user_id = 1234
    store_id = "ST567"

    app = QApplication(sys.argv)
    window = EvaluationForm(user_id=user_id, store_id=store_id)
    window.show()
    sys.exit(app.exec())