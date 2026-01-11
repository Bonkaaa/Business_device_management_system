from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHeaderView, QAbstractItemView, QMessageBox, 
    QDialog, QFormLayout, QComboBox, QLineEdit, QLabel, QGroupBox
)
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtCore import Qt
from src.utils.constant_class import DeviceStatus, DeviceQualityStatus
from datetime import datetime

from utils.validators import DeviceValidator

# --- Class Popup xem chi tiết thiết bị ---
class DeviceDetailDialog(QDialog):
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device
        self.setWindowTitle(f"Chi tiết thiết bị - {device.name}")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Group 1: Thông tin cơ bản
        group_basic = QGroupBox("Thông tin chi tiết")
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Lấy dữ liệu từ object device
        status_info = self.device.get_status()
        status_str = status_info['status'].value if hasattr(status_info['status'], 'value') else str(status_info['status'])
        quality_str = self.device.get_quality_status().value if hasattr(self.device.get_quality_status(), 'value') else str(self.device.get_quality_status())
        assigned_to = status_info.get('assigned_to') or "Chưa được giao"
        if assigned_to != "Chưa được giao":
            assigned_to_name = assigned_to.name
            assigned_to_id = assigned_to.get_id()
            assigned_to_display = f"{assigned_to_name} ({assigned_to_id})"
        else:
            assigned_to_display = "Chưa được giao"

        form.addRow("<b>Mã thiết bị:</b>", QLabel(self.device.get_id()))
        form.addRow("<b>Tên thiết bị:</b>", QLabel(self.device.name))
        form.addRow("<b>Loại:</b>", QLabel(self.device.get_category()))
        form.addRow("<b>Trạng thái:</b>", QLabel(status_str))
        form.addRow("<b>Chất lượng:</b>", QLabel(quality_str))
        form.addRow("<b>Ngày mua:</b>", QLabel(self.device.get_purchase_date()))
        form.addRow("<b>Người sử dụng:</b>", QLabel(assigned_to_display))
        
        group_basic.setLayout(form)
        layout.addWidget(group_basic)

        # Group 2: Thông số kỹ thuật (Specifications)
        group_spec = QGroupBox("Thông số kỹ thuật")
        spec_layout = QVBoxLayout()
        specs = self.device.get_specifications()
        
        spec_text = ""
        if isinstance(specs, dict):
            for k, v in specs.items():
                spec_text += f"• {k}: {v}\n"
        else:
            spec_text = str(specs)
            
        label_spec = QLabel(spec_text if spec_text.strip() else "Không có thông số chi tiết")
        label_spec.setWordWrap(True)
        spec_layout.addWidget(label_spec)
        group_spec.setLayout(spec_layout)
        layout.addWidget(group_spec)

        # Nút đóng
        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.accept)
        btn_close.setFixedWidth(100)
        
        footer = QHBoxLayout()
        footer.addStretch()
        footer.addWidget(btn_close)
        layout.addLayout(footer)

        self.setLayout(layout)


# --- Class chính của tab Quản lý Thiết bị ---
class InventoryTab(QWidget):
    def __init__(self, inventory_manager):
        super().__init__()
        self.inventory_manager = inventory_manager
        self.all_devices = []  
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

        self.btn_add.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px 15px;")
        self.btn_delete.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 5px 15px;")

        toolbar.addWidget(self.btn_load)
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_delete)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # === Filter Bar (Tìm kiếm & Bộ lọc) ===
        filter_bar = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm theo ID, Tên hoặc Người dùng...")
        self.search_input.setFixedWidth(300)
        self.search_input.setFixedHeight(30) # Làm ô search to hơn chút
        self.search_input.textChanged.connect(self.apply_filters)
        
        self.combo_status = QComboBox()
        self.combo_status.setFixedHeight(30)
        self.combo_status.addItems(["-- Trạng thái --", DeviceStatus.AVAILABLE.value, DeviceStatus.ASSIGNED.value, DeviceStatus.MAINTENANCE.value])
        self.combo_status.currentTextChanged.connect(self.apply_filters)

        self.combo_quality = QComboBox()
        self.combo_quality.setFixedHeight(30)
        self.combo_quality.addItems(["-- Chất lượng --", DeviceQualityStatus.GOOD.value, DeviceQualityStatus.BROKEN.value, DeviceQualityStatus.RETIRED.value])
        self.combo_quality.currentTextChanged.connect(self.apply_filters)

        filter_bar.addWidget(QLabel("Tìm kiếm:"))
        filter_bar.addWidget(self.search_input)
        filter_bar.addWidget(QLabel(" Lọc:"))
        filter_bar.addWidget(self.combo_status)
        filter_bar.addWidget(self.combo_quality)
        filter_bar.addStretch()
        layout.addLayout(filter_bar)

        # === Table (Đã làm gọn) ===
        self.table = QTableWidget()
        self.table.setColumnCount(5) # Giảm số cột xuống
        self.table.setHorizontalHeaderLabels(["ID", "Tên thiết bị", "Loại", "Trạng thái", "Chất lượng"])

        # Cấu hình UI cho Table
        font = QFont()
        font.setPointSize(11) # Tăng cỡ chữ bảng
        self.table.setFont(font)
        self.table.verticalHeader().setDefaultSectionSize(40) # Tăng chiều cao dòng
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet("font-weight: bold;")

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True) 
        
        # --- SỰ KIỆN CLICK ---
        self.table.cellDoubleClicked.connect(self.show_device_details)

        layout.addWidget(self.table)
        
        # Gợi ý nhỏ ở dưới
        layout.addWidget(QLabel("<i>* Nhấp đúp vào một dòng để xem chi tiết đầy đủ của thiết bị.</i>"))

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            if hasattr(self.inventory_manager, 'get_all_devices'):
                all_devices = self.inventory_manager.get_all_devices()
                # Filter out None devices
                self.all_devices = [d for d in all_devices if d is not None]
            self.apply_filters()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {e}")

    def apply_filters(self):
        search_text = self.search_input.text().lower()
        status_filter = self.combo_status.currentText()
        quality_filter = self.combo_quality.currentText()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for device in self.all_devices:
            # Skip None devices
            if device is None:
                continue
                
            d_id = device.get_id().lower()
            d_name = device.name.lower()
            
            status_info = device.get_status()
            d_status = status_info['status'].value if hasattr(status_info['status'], 'value') else str(status_info['status'])
            assigned_to = str(status_info.get('assigned_to') or "Chưa được giao").lower()
            
            quality_val = device.get_quality_status()
            d_quality = quality_val.value if hasattr(quality_val, 'value') else str(quality_val)

            match_search = (search_text in d_id or search_text in d_name or search_text in assigned_to)
            match_status = (status_filter == "-- Trạng thái --" or status_filter == d_status)
            match_quality = (quality_filter == "-- Chất lượng --" or quality_filter == d_quality)

            if match_search and match_status and match_quality:
                self.add_row_to_table(device)

        self.table.setSortingEnabled(True)

    def add_row_to_table(self, device):
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        
        # Chỉ hiển thị 4 cột cho gọn
        self.table.setItem(row_idx, 0, QTableWidgetItem(device.get_id()))
        self.table.setItem(row_idx, 1, QTableWidgetItem(device.name))
        self.table.setItem(row_idx, 2, QTableWidgetItem(device.get_category()))
        
        # Trạng thái (hiển thị màu tinh tế hơn)
        status_val = device.get_status()['status']
        status_str = status_val.value if hasattr(status_val, 'value') else str(status_val)
        item_status = QTableWidgetItem(status_str)
        
        if status_str == DeviceStatus.AVAILABLE.value:
            item_status.setBackground(QBrush(QColor(144, 238, 144)))  # Light green
            item_status.setForeground(QBrush(QColor(0, 0, 0)))  
        elif status_str == DeviceStatus.ASSIGNED.value:
            item_status.setBackground(QBrush(QColor("#F9FD00")))  # Yellow
            item_status.setForeground(QBrush(QColor(0, 0, 0))) 
        elif status_str == DeviceStatus.MAINTENANCE.value:
            item_status.setBackground(QBrush(QColor("#FF0D0D")))  # Red
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

    def show_device_details(self, row, column):
        """Hàm mở popup khi nhấp đúp vào dòng"""
        device_id = self.table.item(row, 0).text()
        # Tìm đối tượng device tương ứng
        device = next((d for d in self.all_devices if d.get_id() == device_id), None)
        
        if device:
            dialog = DeviceDetailDialog(device, self)
            dialog.exec()

    def open_add_device_dialog(self):
        dialog = AddDeviceDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                device = self.inventory_manager.add_device(
                    name=data['name'],
                    category=data['category'],
                    purchase_date=data['purchase_date'],
                    specifications=data['specifications']
                )
                QMessageBox.information(self, "Thành công", "Đã thêm thiết bị mới!")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi: {e}")

    def delete_selected_device(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn thiết bị.")
            return
        
        device_id = self.table.item(current_row, 0).text()
        device = self.inventory_manager.get_device_by_id(device_id)
        if not device:
            QMessageBox.critical(self, "Lỗi", "Thiết bị không tồn tại.")
            return
        assignee_id = device.get_status().get('assigned_to')

        confirm = QMessageBox.question(self, "Xác nhận", f"Xóa thiết bị {device_id}?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Remove assign_devices in assignees first (only if device is assigned)
                if assignee_id is not None:
                    self.inventory_manager.hr_manager.remove_device_from_assigned_devices_list_of_assignee(assignee_id, device_id)

                # Close any active assignments related to this device
                assignment = self.inventory_manager.assignment_manager.get_active_assignment_by_device_id(device_id)
                if assignment:
                    self.inventory_manager.assignment_manager.close_assignment(
                        assignment_id=assignment.get_id(),
                        return_quality_status=DeviceQualityStatus.RETIRED,
                        actual_return_date=datetime.now().isoformat(),
                        broken_status=True
                    )
                # Finally, remove device from database
                self.inventory_manager.remove_device(device_id)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

# (Giữ nguyên class AddDeviceDialog của bạn bên dưới)
class AddDeviceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm thiết bị mới")
        self.setFixedSize(450, 200)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Ví dụ: Laptop Dell XPS 13")

        self.input_category = QLineEdit()
        self.input_category.setPlaceholderText("Ví dụ: Laptop, Điện thoại, Máy in...")

        self.input_purchase_date = QLineEdit()
        self.input_purchase_date.setPlaceholderText("Định dạng: YYYY-MM-DD")

        self.input_specifications = QLineEdit()
        self.input_specifications.setPlaceholderText('Ví dụ: {"CPU": "Intel i7", "RAM": "16GB"}')


        layout.addRow("Tên Thiết bị:", self.input_name)
        layout.addRow("Loại Thiết bị:", self.input_category)
        layout.addRow("Ngày Mua:", self.input_purchase_date)
        layout.addRow("Thông số Kỹ thuật (JSON):", self.input_specifications)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.handle_save)
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
    
    def handle_save(self):
        name = self.input_name.text().strip()
        category = self.input_category.text().strip()
        purchase_date = self.input_purchase_date.text().strip()
        specifications = self.input_specifications.text().strip()

        valid = DeviceValidator.validate_device_input(
            name=name,
            category=category,
            purchase_date=purchase_date,
            specifications=specifications
        )

        if valid is not True:
            QMessageBox.warning(self, "Lỗi khi nhập dữ liệu", valid)
            return
        
        self.accept()