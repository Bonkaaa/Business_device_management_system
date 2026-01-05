from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from .inventory_tab import InventoryTab
from .hr_tab import HRTab

class MainWindow(QMainWindow):
    def __init__(self, inventory, hr, assignment, maintenance):
        super().__init__()
        
        self.inventory_manager = inventory
        self.hr_manager = hr
        self.assignment_manager = assignment
        self.maintenance_manager = maintenance

        self.setWindowTitle("Hệ Thống Quản Lý Thiết Bị CNTT")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab Inventory
        self.tab_inventory = InventoryTab(self.inventory_manager)
        self.tabs.addTab(self.tab_inventory, "📦 Kho Thiết Bị")

        # Tab HR
        self.tab_hr = HRTab(self.hr_manager)
        self.tabs.addTab(self.tab_hr, "👥 Quản Lý Nhân Sự")
