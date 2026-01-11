# File: src/ui/register_window.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from utils.constant_class import UserRole

class RegisterWindow(QWidget):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setWindowTitle("Đăng Ký Tài Khoản Mới")
        self.setFixedSize(400, 450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        # Title
        lbl_title = QLabel("ĐĂNG KÝ")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #FF9800;") # Màu cam
        layout.addWidget(lbl_title)

        # Inputs
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Tên đăng nhập (*)")
        self.txt_username.setFixedHeight(40)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Mật khẩu (*)")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setFixedHeight(40)

        self.txt_confirm_pass = QLineEdit()
        self.txt_confirm_pass.setPlaceholderText("Nhập lại mật khẩu (*)")
        self.txt_confirm_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_confirm_pass.setFixedHeight(40)
        
        self.txt_emp_id = QLineEdit()
        self.txt_emp_id.setPlaceholderText("Mã nhân viên (Nếu có)")
        self.txt_emp_id.setToolTip("Nhập mã nhân viên của bạn để xem dữ liệu cá nhân")
        self.txt_emp_id.setFixedHeight(40)

        layout.addWidget(self.txt_username)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.txt_confirm_pass)
        layout.addWidget(self.txt_emp_id)

        # Buttons
        self.btn_register = QPushButton("TẠO TÀI KHOẢN")
        self.btn_register.setFixedHeight(45)
        self.btn_register.setStyleSheet("""
            QPushButton {
                background-color: #FF9800; 
                color: white; 
                font-weight: bold; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.btn_register.clicked.connect(self.handle_register)
        layout.addWidget(self.btn_register)
        
        self.btn_cancel = QPushButton("Quay lại Đăng nhập")
        self.btn_cancel.setStyleSheet("border: none; color: #555; text-decoration: underline;")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.close)
        layout.addWidget(self.btn_cancel)

        self.setLayout(layout)

    def handle_register(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()
        confirm = self.txt_confirm_pass.text().strip()
        emp_id = self.txt_emp_id.text().strip()

        # 1. Validate cơ bản
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Tên đăng nhập và Mật khẩu.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp.")
            return

        # 2. Check trùng user
        if self.auth_manager.check_username_exists(username):
            QMessageBox.critical(self, "Lỗi", f"Tài khoản '{username}' đã tồn tại!")
            return

        # 3. Tạo tài khoản (Mặc định Role EMPLOYEE)
        # Nếu user không nhập emp_id thì gửi None
        final_emp_id = emp_id if emp_id else None
        
        success = self.auth_manager.create_account(
            username=username, 
            password=password, 
            role=UserRole.EMPLOYEE, 
            employee_id=final_emp_id
        )

        if success:
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
            self.close()
        else:
            QMessageBox.critical(self, "Lỗi", "Có lỗi xảy ra khi tạo tài khoản.")