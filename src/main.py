import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from manager import Inventory, HRManager, AssignmentManager, MaintenanceManager, AuthManager
from ui import MainWindow, LoginWindow
from utils.constant_class import UserRole
from utils.login_window_utils import create_default_accounts

def main():
    print("Đang khởi động ứng dụng Quản lý Thiết bị CNTT...")
    app = QApplication(sys.argv)

    # Xác định đường dẫn thư mục data và tạo nếu chưa có
    if getattr(sys, 'frozen', False):
        # Chạy từ file .exe (PyInstaller)
        base_dir = os.path.dirname(sys.executable)
    else:
        # Chạy từ Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    db_path = os.path.join(data_dir, "sharedatabase.db")
    print(f"Database path: {db_path}")

    # Thiết lập cơ sở dữ liệu và tạo tài khoản admin mặc định nếu cần
    auth_manager = AuthManager(db_path=db_path)
    hr_manager = HRManager(db_path=db_path)
    inventory_manager = Inventory(db_path=db_path)
    assignment_manager = AssignmentManager(db_path=db_path)
    maintenance_manager = MaintenanceManager(db_path=db_path)

    # Thiết lập tham chiếu chéo giữa các manager
    hr_manager.set_managers(inventory_manager, assignment_manager)
    inventory_manager.set_managers(hr_manager, assignment_manager)
    assignment_manager.set_managers(inventory_manager, hr_manager)
    maintenance_manager.set_managers(inventory_manager, hr_manager)

    # Tạo tài khoản admin mặc định nếu chưa có
    create_default_accounts(auth_manager)

    current_window = None

    def show_login():
        nonlocal current_window
        login_window = LoginWindow(auth_manager)
        login_window.login_success.connect(show_main_window) 
        current_window = login_window
        login_window.show()

    def show_main_window(user_info):
        nonlocal current_window
        # Đóng login window cũ nếu có
        if current_window:
            current_window.close()
            
        print(f"User {user_info['username']} logged in.")
        
        main_window = MainWindow(
            inventory=inventory_manager,
            hr=hr_manager,
            assignment=assignment_manager,
            maintenance=maintenance_manager,
            auth_manager=auth_manager, 
            current_user=user_info
        )
        
        # Kết nối tín hiệu logout -> gọi lại show_login
        main_window.logout_signal.connect(show_login)
        
        main_window.setWindowTitle(f"Quản Lý Thiết Bị - {user_info['username']} ({user_info['role']})")
        current_window = main_window
        main_window.show()

    show_login()

    print("Ứng dụng đã sẵn sàng sử dụng.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()