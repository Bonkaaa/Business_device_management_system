import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from manager import Inventory, HRManager, AssignmentManager, MaintenanceManager
from ui import MainWindow

def main():
    print("Đang khởi động ứng dụng Quản lý Thiết bị CNTT...")
    hr_manager = HRManager(db_path="data/hr_database.db")
    inventory_manager = Inventory(db_path="data/inventory_database.db", hr_manager=hr_manager)
    assignment_manager = AssignmentManager(db_path="data/assignment_database.db", inventory_manager=inventory_manager, hr_manager=hr_manager)
    maintenance_manager = MaintenanceManager(db_path="data/maintenance_database.db", inventory_manager=inventory_manager, hr_manager=hr_manager)

    app = QApplication(sys.argv)

    window = MainWindow(
        inventory=inventory_manager,
        hr=hr_manager,
        assignment=assignment_manager,
        maintenance=maintenance_manager,
    )
    window.show()

    print("Ứng dụng đã sẵn sàng sử dụng.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()