from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHeaderView, QAbstractItemView, QMessageBox, 
    QDialog, QFormLayout, QComboBox, QLineEdit
)
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtCore import Qt
from src.utils.constant_class import DeviceStatus, DeviceQualityStatus
from datetime import datetime

class InventoryTab(QWidget):
    def __init__(self, inventory_manager):
        super().__init__()
        self.inventory_manager = inventory_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # === Toolbar ===
        toolbar = QHBoxLayout()

        self.btn_load = QPushButton("🔄 Làm mới")
        self.btn_load.clicked.connect(self.load_data)

        self.btn_add = QPushButton("➕ Thêm thiết bị")
        self.btn_add.clicked.connect(self.open_add_device_dialog)

        self.btn_delete = QPushButton("🗑️ Xóa thiết bị")
        self.btn_delete.clicked.connect(self.delete_selected_device)

        self.btn_add.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_delete.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")

        toolbar.addWidget(self.btn_load)
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_delete)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # === Table ===
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên", "Loại", "Trạng thái", "Chất lượng", "Ngày mua", "Người dùng"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.table.setAlternatingRowColors(False)
        self.table.setStyleSheet("") 

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        try:
            if hasattr(self.inventory_manager, 'get_all_devices'):
                devices = self.inventory_manager.get_all_devices()
            
            self.table.setRowCount(0)
    
            for row_idx, device in enumerate(devices):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(device.get_id()))
                self.table.setItem(row_idx, 1, QTableWidgetItem(device.name))
                self.table.setItem(row_idx, 2, QTableWidgetItem(device.category))
                
                # Status
                status_val = device.get_status()['status']
                status_str = status_val.value if hasattr(status_val, 'value') else str(status_val)
                item_status = QTableWidgetItem(status_str)
    
                if status_str == DeviceStatus.AVAILABLE.value:
                    item_status.setBackground(QBrush(QColor(144, 238, 144)))  # Light green
                    item_status.setForeground(QBrush(QColor(0, 0, 0)))  
                elif status_str == DeviceStatus.ASSIGNED.value:
                    item_status.setBackground(QBrush(QColor(255, 255, 224)))  # Light yellow
                    item_status.setForeground(QBrush(QColor(0, 0, 0))) 
                elif status_str == DeviceStatus.MAINTENANCE.value:
                    item_status.setBackground(QBrush(QColor(255, 182, 193)))  # Light red
                    item_status.setForeground(QBrush(QColor(0, 0, 0))) 
    
                self.table.setItem(row_idx, 3, item_status)
    
                # Quality Status
                quality_status_val = device.get_quality_status()
                quality_status_str = quality_status_val.value if hasattr(quality_status_val, 'value') else str(quality_status_val)
                item_quality = QTableWidgetItem(quality_status_str)
    
                if quality_status_str == DeviceQualityStatus.GOOD.value:
                    item_quality.setBackground(QBrush(QColor(144, 238, 144)))  # Light green
                    item_quality.setForeground(QBrush(QColor(0, 0, 0)))
                elif quality_status_str == DeviceQualityStatus.BROKEN.value:
                    item_quality.setBackground(QBrush(QColor(255, 182, 193)))  # Light red
                    item_quality.setForeground(QBrush(QColor(0, 0, 0)))
                elif quality_status_str == DeviceQualityStatus.RETIRED.value:
                    item_quality.setBackground(QBrush(QColor(211, 211, 211)))  # Light gray
                    item_quality.setForeground(QBrush(QColor(0, 0, 0)))
                self.table.setItem(row_idx, 4, item_quality)
                
                # Purchase Date
                purchase_date_str = device.get_purchase_date()
                self.table.setItem(row_idx, 5, QTableWidgetItem(purchase_date_str))
                
                # Assigned To
                assigned_to = device.get_status().get('assigned_to')
                if assigned_to is None:
                    assigned_to = "Chưa được giao"
                self.table.setItem(row_idx, 6, QTableWidgetItem(str(assigned_to)))
                if assigned_to == "Chưa được giao":
                    self.table.item(row_idx, 6).setForeground(QBrush(QColor(128, 128, 128)))  # Gray color
                else:
                    self.table.item(row_idx, 6).setForeground(QBrush(QColor(0, 0, 0)))  # Black color

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu thiết bị: {e}")

    
    def open_add_device_dialog(self):
        dialog = AddDeviceDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                purcharse_date = None
                if data['purchase_date']:
                    purcharse_date = datetime.strptime(data['purchase_date'], "%Y-%m-%d").date()

                device = self.inventory_manager.add_device(
                    name=data['name'],
                    category=data['category'],
                    purchase_date=data['purchase_date'],
                    specifications=data['specifications']
                )
                QMessageBox.information(self, "Thành công", f"Đã thêm thiết bị mới thành công!\nID:{device.get_id()}")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể thêm thiết bị: {e}")

    def delete_selected_device(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một thiết bị để xóa.")
            return
        
        device_id = self.table.item(current_row, 0).text()

        confirm = QMessageBox.question(
            self, "Xác nhận", 
            f"Bạn có chắc chắn muốn xóa thiết bị với ID {device_id} không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.inventory_manager.remove_device(device_id)
                QMessageBox.information(self, "Thành công", "Đã xóa thiết bị thành công!")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa thiết bị: {e}")

class AddDeviceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm thiết bị mới")
        self.setFixedSize(350, 250)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.input_device_id = QLineEdit()
        self.input_name = QLineEdit()
        self.input_category = QLineEdit()
        self.input_purchase_date = QLineEdit()
        self.input_specifications = QLineEdit()

        layout.addRow("Tên Thiết bị:", self.input_name)
        layout.addRow("Loại Thiết bị:", self.input_category)
        layout.addRow("Ngày Mua (YYYY-MM-DD):", self.input_purchase_date)
        layout.addRow("Thông số Kỹ thuật (JSON):", self.input_specifications)

        # Buttons
        btn_box = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.accept)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)

        btn_box.addWidget(btn_save)
        btn_box.addWidget(btn_cancel)

        layout.addRow(btn_box)

        self.setLayout(layout)

    def get_data(self):
        return {
            'name': self.input_name.text(),
            'category': self.input_category.text(),
            'purchase_date': self.input_purchase_date.text(),
            'specifications': self.input_specifications.text(),
        }


