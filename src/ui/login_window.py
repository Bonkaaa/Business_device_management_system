# File: src/ui/login_window.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class LoginWindow(QWidget):
    login_success = pyqtSignal(dict) # Signal gửi thông tin user khi login thành công

    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setWindowTitle("Đăng nhập Hệ thống")
        # self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Title
        lbl_title = QLabel("HỆ THỐNG QUẢN LÝ THIẾT BỊ CNTT")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_title = QFont("Arial", 20, QFont.Weight.Bold)
        lbl_title.setFont(font_title)
        lbl_title.setStyleSheet("color: #2196F3;")
        layout.addWidget(lbl_title)

        # Input fields
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Tên đăng nhập")
        self.txt_username.setFixedHeight(40)
        
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Mật khẩu")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setFixedHeight(40)
        self.txt_password.returnPressed.connect(self.handle_login) # Enter để login

        layout.addWidget(self.txt_username)
        layout.addWidget(self.txt_password)

        # Button
        self.btn_login = QPushButton("ĐĂNG NHẬP")
        self.btn_login.setFixedHeight(45)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-weight: bold; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btn_login.clicked.connect(self.handle_login)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def handle_login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        user = self.auth_manager.login(username, password)
        if user:
            self.login_success.emit(user)
            self.close()
        else:
            QMessageBox.critical(self, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")