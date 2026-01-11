from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from PyQt6.QtGui import QAction 
from PyQt6.QtCore import pyqtSignal
from .inventory_tab import InventoryTab
from .hr_tab import HRTab
from .assignment_tab import AssignmentTab
from .maintenance_tab import MaintenanceTab
from .dashboard_tab import DashboardTab
from .change_password_dialog import ChangePasswordDialog
from utils.constant_class import UserRole

class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self, inventory, hr, assignment, maintenance, auth_manager, current_user):
        super().__init__()
        
        self.inventory_manager = inventory
        self.hr_manager = hr
        self.assignment_manager = assignment
        self.maintenance_manager = maintenance
        self.auth_manager = auth_manager

        # User info and role
        self.current_user = current_user
        self.user_role = current_user['role'] if current_user else 'guest'

        self.setWindowTitle("Hệ Thống Quản Lý Thiết Bị CNTT")
        self.resize(1200, 800)
        
        self.init_menu() # <--- Gọi hàm tạo menu
        self.init_ui()

        self.apply_role_permissions()

    def init_menu(self):
        menu_bar = self.menuBar()
        
        # Menu Tài khoản
        account_menu = menu_bar.addMenu("👤 Tài khoản")
        
        # Action Đổi mật khẩu
        action_change_pass = QAction("Đổi mật khẩu", self)
        action_change_pass.triggered.connect(self.open_change_password)
        account_menu.addAction(action_change_pass)
        
        account_menu.addSeparator()
        
        # Action Đăng xuất
        action_logout = QAction("Đăng xuất", self)
        action_logout.triggered.connect(self.handle_logout)
        account_menu.addAction(action_logout)

    def init_ui(self):
        self.setWindowTitle("Hệ Thống Quản Lý Thiết Bị CNTT")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.tabs.currentChanged.connect(self.on_tab_changed)

        # Tab Dashboard
        self.tab_dashboard = DashboardTab(self.inventory_manager, self.hr_manager, self.assignment_manager, self.maintenance_manager)
        self.tabs.addTab(self.tab_dashboard, "📊 Bảng Điều Khiển")

        # Tab Inventory
        self.tab_inventory = InventoryTab(self.inventory_manager)
        self.tabs.addTab(self.tab_inventory, "📦 Kho Thiết Bị")

        # Tab HR
        self.tab_hr = HRTab(self.hr_manager)
        self.tabs.addTab(self.tab_hr, "👥 Quản Lý Nhân Sự")

        # Tab Assignments
        self.tab_assignments = AssignmentTab(self.assignment_manager, self.inventory_manager, self.hr_manager, self.current_user)
        self.tabs.addTab(self.tab_assignments, "📝 Quản Lý Giao Thiết Bị")

        self.tab_assignments.data_changed.connect(self.tab_inventory.load_data)

        # Tab Maintenance
        self.tab_maintenance = MaintenanceTab(self.maintenance_manager, self.inventory_manager, self.hr_manager, self.current_user)
        self.tabs.addTab(self.tab_maintenance, "🛠️ Bảo trì")

    def open_change_password(self):
        dialog = ChangePasswordDialog(self.auth_manager, self)
        dialog.exec()

    def handle_logout(self):
        confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn đăng xuất?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit() # Gửi tín hiệu về main.py
            self.close()

    def apply_role_permissions(self):
        role = self.user_role

        # ---1. Admin ---
        if role == UserRole.ADMIN.value:
            pass

        # ---2. Technician ---
        elif role == UserRole.TECHNICIAN.value:
            # Tab HR và Dashboard: Vô hiệu hóa
            self.tabs.setTabVisible(0, False)  
            self.tabs.setTabVisible(1, False)  # 1 là index của tab HR

            # Tab Inventory: Chỉ xem
            self.tab_inventory.btn_add.hide()
            self.tab_inventory.btn_delete.hide()

            # Tab Assignments: Chỉ xem
            self.tab_assignments.btn_create.hide()
            self.tab_assignments.btn_return.hide()

        # ---3. Employee ---
        elif role == UserRole.EMPLOYEE.value:
            # Tab HR và Dashboard: Vô hiệu hóa
            self.tabs.setTabVisible(0, False)  
            self.tabs.setTabVisible(1, False)  # 1 là index của tab HR

            # Tab Inventory: Chỉ xem
            self.tab_inventory.btn_add.hide()
            self.tab_inventory.btn_delete.hide()
            self.tab_inventory.btn_load.show()

            # Tab Maintenance
            self.tab_maintenance.btn_resolve.hide()     # Nút Cập nhật xử lý
            self.tab_maintenance.btn_close_ticket.hide() # Nút Đóng phiếu
            self.tab_maintenance.btn_load.show()
            self.tab_maintenance.btn_report.show()

    def on_tab_changed(self, index):
        if index == 0:  # Dashboard tab
            self.tab_dashboard.load_data()

        elif self.tabs.widget(index) == self.tab_inventory:
            self.tab_inventory.load_data()
        
        elif self.tabs.widget(index) == self.tab_assignments:
            self.tab_assignments.load_data()
        
        elif self.tabs.widget(index) == self.tab_maintenance:
            self.tab_maintenance.load_data()

