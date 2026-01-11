# File: src/ui/change_password_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout

class ChangePasswordDialog(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.setWindowTitle("Đổi Mật Khẩu")
        self.setFixedSize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.txt_old_pass = QLineEdit()
        self.txt_old_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.txt_new_pass = QLineEdit()
        self.txt_new_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.txt_confirm_pass = QLineEdit()
        self.txt_confirm_pass.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Mật khẩu cũ:", self.txt_old_pass)
        form.addRow("Mật khẩu mới:", self.txt_new_pass)
        form.addRow("Xác nhận mới:", self.txt_confirm_pass)
        
        layout.addLayout(form)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Lưu thay đổi")
        btn_save.clicked.connect(self.save_password)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)
        
        btn_box.addWidget(btn_save)
        btn_box.addWidget(btn_cancel)
        layout.addLayout(btn_box)

        self.setLayout(layout)

    def save_password(self):
        old_pass = self.txt_old_pass.text()
        new_pass = self.txt_new_pass.text()
        confirm_pass = self.txt_confirm_pass.text()

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        current_user = self.auth_manager.get_current_user()
        if not current_user:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy thông tin người dùng!")
            return

        username = current_user['username']
        if self.auth_manager.change_password(username, old_pass, new_pass):
            QMessageBox.information(self, "Thành công", "Đổi mật khẩu thành công!")
            self.accept()
        else:
            QMessageBox.critical(self, "Lỗi", "Mật khẩu cũ không chính xác!")