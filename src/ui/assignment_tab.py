# File: src/ui/assignment_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHeaderView, QAbstractItemView, QMessageBox, 
    QDialog, QFormLayout, QComboBox, QDateEdit, QLabel, QCheckBox, QGroupBox, QLineEdit
)
from datetime import datetime
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QColor, QBrush, QFont
from src.utils.constant_class import AssignmentStatus, DeviceQualityStatus, UserRole

# === 1. Popup Chi tiết Phiếu Giao ===
class AssignmentDetailDialog(QDialog):
    def __init__(self, assignment, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Chi tiết phiếu: {assignment.get_id()}")
        self.setMinimumWidth(450)
        self.init_ui(assignment)

    def init_ui(self, ass):
        layout = QVBoxLayout()
        group = QGroupBox("Thông tin phiếu giao/trả")
        form = QFormLayout()

        dev_name = ass.get_device().name if ass.get_device() else "N/A"
        dev_id = ass.get_device().get_id() if ass.get_device() else "N/A"
        dev_display = f"{dev_name} ({dev_id})"

        assignee_name = ass.get_assignee().name if ass.get_assignee() else "N/A"
        
        status_val = ass.get_status()
        status_str = status_val.value if hasattr(status_val, 'value') else str(status_val)

        form.addRow("<b>Mã phiếu:</b>", QLabel(ass.get_id()))
        form.addRow("<b>Nhân viên/Phòng ban:</b>", QLabel(assignee_name))
        form.addRow("<b>Thiết bị:</b>", QLabel(dev_display)) 
        form.addRow("<b>Trạng thái:</b>", QLabel(status_str))
        
        init_date = ass.get_initial_date().strftime("%d/%m/%Y") if ass.get_initial_date() else "N/A"
        exp_date = ass.get_expected_return_date().strftime("%d/%m/%Y") if ass.get_expected_return_date() else "N/A"
        act_date = ass.get_actual_return_date().strftime("%d/%m/%Y") if ass.get_actual_return_date() else "Chưa trả"
        
        form.addRow("<b>Ngày giao:</b>", QLabel(init_date))
        form.addRow("<b>Hạn trả dự kiến:</b>", QLabel(exp_date))
        form.addRow("<b>Ngày trả thực tế:</b>", QLabel(act_date))

        group.setLayout(form)
        layout.addWidget(group)

        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

# === 2. Tab Assignment Chính ===
class AssignmentTab(QWidget):
    data_changed = pyqtSignal()
    def __init__(self, assignment_manager, inventory_manager, hr_manager, current_user):
        super().__init__()
        self.assignment_manager = assignment_manager
        self.inventory_manager = inventory_manager
        self.hr_manager = hr_manager
        self.current_user = current_user
        self.all_assignments = []
        self.init_ui()

        self.apply_role_permissions()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- Toolbar ---
        toolbar = QHBoxLayout()
        self.btn_load = QPushButton("🔄 Làm mới")
        self.btn_create = QPushButton("➕ Tạo phiếu mới")
        self.btn_return = QPushButton("↩️ Trả thiết bị")
        
        self.btn_create.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px 15px;")
        self.btn_return.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 5px 15px;")
        
        # [ĐÃ XÓA] Checkbox "Hiển thị cả phiếu đã đóng"

        toolbar.addWidget(self.btn_load)
        toolbar.addWidget(self.btn_create)
        toolbar.addWidget(self.btn_return)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # --- Filter Bar ---
        filter_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm theo Mã phiếu, Nhân viên, Thiết bị...")
        self.search_input.setFixedHeight(30)
        self.search_input.textChanged.connect(self.apply_filters)

        self.combo_status = QComboBox()
        self.combo_status.setFixedHeight(30)
        # Thêm các tùy chọn lọc
        self.combo_status.addItems(["-- Tất cả trạng thái --", AssignmentStatus.OPEN.value, AssignmentStatus.OVERDUE.value, AssignmentStatus.CLOSED.value])
        self.combo_status.currentTextChanged.connect(self.apply_filters)

        filter_bar.addWidget(QLabel("Tìm kiếm:"))
        filter_bar.addWidget(self.search_input, 3)
        filter_bar.addWidget(QLabel("Lọc:"))
        filter_bar.addWidget(self.combo_status, 1)
        layout.addLayout(filter_bar)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Mã Phiếu", "Đối Tượng", "Thiết Bị", "Trạng Thái"])
        
        font = QFont()
        font.setPointSize(10)
        self.table.setFont(font)
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        # Sự kiện
        self.btn_load.clicked.connect(self.load_data)
        self.btn_create.clicked.connect(self.open_create_dialog)
        self.btn_return.clicked.connect(self.open_return_dialog)
        self.table.cellDoubleClicked.connect(self.show_detail)

        layout.addWidget(self.table)
        layout.addWidget(QLabel("<i>* Nhấp đúp vào một dòng để xem chi tiết thời hạn và lịch sử trả.</i>"))
        self.setLayout(layout)
        
        # Gọi load_data ngay khi khởi tạo xong
        self.load_data()

    def apply_role_permissions(self):
        # Nếu là nhân viên -> Ẩn nút tạo và trả
        if self.current_user['role'] == UserRole.EMPLOYEE.value:
            self.btn_create.hide()
            self.btn_return.hide()

    def load_data(self):
        try:
            is_employee = self.current_user['role'] == UserRole.EMPLOYEE.value
            emp_id = self.current_user.get('employee_id', None)
            
            # [SỬA LOGIC] Luôn lấy toàn bộ danh sách (cả cũ và mới)
            # Bộ lọc ComboBox sẽ lo việc hiển thị cái gì
            if is_employee and emp_id:
                # Lấy tất cả phiếu của nhân viên này
                # Lưu ý: Cần đảm bảo AssignmentManager có hàm get_assignments_by_assignee_id hoặc get_all_assignments_by_assignee_id trả về list
                self.all_assignments = self.assignment_manager.get_assignments_by_assignee_id(emp_id)
            else:
                # Lấy tất cả phiếu hệ thống
                self.all_assignments = self.assignment_manager.get_all_assignments()

            if self.all_assignments is None:
                self.all_assignments = []

            # [FIX QUAN TRỌNG] Phải gọi hàm này để vẽ dữ liệu lên bảng
            self.apply_filters()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {e}")

    def apply_filters(self):
        search_text = self.search_input.text().lower()
        status_filter = self.combo_status.currentText()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for ass in self.all_assignments:
            assignee_name = ass.get_assignee().name if ass.get_assignee() else "N/A"
            device_name = ass.get_device().name if ass.get_device() else "N/A"
            
            status_val = ass.get_status()
            status_str = status_val.value if hasattr(status_val, 'value') else str(status_val)

            match_search = (search_text in ass.get_id().lower() or 
                            search_text in assignee_name.lower() or 
                            search_text in device_name.lower())
            
            # Logic lọc trạng thái
            match_status = (status_filter == "-- Tất cả trạng thái --" or status_filter == status_str)

            if match_search and match_status:
                self.add_row(ass, assignee_name, device_name, status_str)

        self.table.setSortingEnabled(True)

    def add_row(self, ass, assignee_name, device_name, status_str):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(ass.get_id()))
        self.table.setItem(row, 1, QTableWidgetItem(assignee_name))
        self.table.setItem(row, 2, QTableWidgetItem(device_name))
        
        item_status = QTableWidgetItem(status_str)
        if status_str == AssignmentStatus.OPEN.value:
            item_status.setBackground(QBrush(QColor(144, 238, 144)))  # Light green
            item_status.setForeground(QBrush(QColor(0, 0, 0)))
        elif status_str == AssignmentStatus.OVERDUE.value:
            item_status.setBackground(QBrush(QColor(255, 255, 224)))  # Light yellow
            item_status.setForeground(QBrush(QColor(0, 0, 0))) 
        else:
            item_status.setBackground(QBrush(QColor("#e0e0e0"))) # Xám cho đã đóng
            item_status.setForeground(QBrush(QColor(0, 0, 0)))
            
        self.table.setItem(row, 3, item_status)

    def show_detail(self, row, col):
        ass_id = self.table.item(row, 0).text()
        ass = next((a for a in self.all_assignments if a.get_id() == ass_id), None)
        if ass:
            AssignmentDetailDialog(ass, self).exec()

    def open_create_dialog(self):
        available_devices = self.inventory_manager.get_all_available_devices()
        employees = self.hr_manager.get_all_employees()
        departments = self.hr_manager.get_all_departments()

        if not available_devices:
            QMessageBox.warning(self, "Cảnh Báo", "Không có thiết bị sẵn sàng.")
            return
        
        dialog = CreateAssignmentDialog(available_devices, employees, departments, self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                quality_status = data["device"].get_quality_status()
                self.assignment_manager.create_assignment(
                    device=data["device"],
                    assignee=data["assignee"],
                    expected_return_date=data["expected_return_date"],
                    quality_status=quality_status
                )
                self.load_data()
                self.data_changed.emit()
                QMessageBox.information(self, "Thành Công", "Đã giao thiết bị.")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def open_return_dialog(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Cảnh Báo", "Vui lòng chọn phiếu cần trả.")
            return
        
        assignment_id = self.table.item(current_row, 0).text()
        status_text = self.table.item(current_row, 3).text()

        if status_text == AssignmentStatus.CLOSED.value:
            QMessageBox.warning(self, "Thông Báo", "Phiếu này đã hoàn thành trước đó.")
            return
        
        dialog = ReturnAssignmentDialog(assignment_id, self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.assignment_manager.close_assignment(
                    assignment_id=assignment_id,
                    return_quality_status=data["return_quality_status"],
                    broken_status=data["broken_status"],
                    actual_return_date=data["actual_return_date"]
                )
                self.load_data()
                self.data_changed.emit()
                QMessageBox.information(self, "Thành Công", "Đã nhận lại thiết bị.")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

# === 3. Các Dialogs ===

class CreateAssignmentDialog(QDialog):
    def __init__(self, devices, employees, departments, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tạo Phiếu Giao")
        self.setFixedSize(400, 250)
        layout = QFormLayout()

        self.device_combo = QComboBox()
        for dev in devices:
            self.device_combo.addItem(f"{dev.get_id()} - {dev.name}", dev)

        self.assignee_combo = QComboBox()
        for emp in employees:
            self.assignee_combo.addItem(f"👤 {emp.name}", emp)
        for dept in departments:
            self.assignee_combo.addItem(f"🏢 {dept.get_name()}", dept)
        
        self.return_date_edit = QDateEdit()
        self.return_date_edit.setCalendarPopup(True)
        self.return_date_edit.setDate(QDate.currentDate().addMonths(3))
        
        layout.addRow("Chọn Thiết Bị:", self.device_combo)
        layout.addRow("Người nhận:", self.assignee_combo)
        layout.addRow("Hạn trả dự kiến:", self.return_date_edit)

        btn_box = QHBoxLayout()
        btn_ok = QPushButton("Xác nhận"); btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Hủy"); btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_ok); btn_box.addWidget(btn_cancel)
        layout.addRow(btn_box)
        self.setLayout(layout)

    def get_data(self):
        return {
            "device": self.device_combo.currentData(),
            "assignee": self.assignee_combo.currentData(),
            "expected_return_date": self.return_date_edit.date().toPyDate()
        }

class ReturnAssignmentDialog(QDialog):
    def __init__(self, assignment_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Trả Thiết Bị {assignment_id}")
        self.setFixedSize(350, 200)

        layout = QFormLayout()

        # Quality ComboBox
        self.quality_combo = QComboBox()
        self.quality_combo.addItem("Tốt", DeviceQualityStatus.GOOD)
        self.quality_combo.addItem("Hỏng", DeviceQualityStatus.BROKEN)
        self.quality_combo.addItem("Thanh Lý", DeviceQualityStatus.RETIRED)

        self.check_broken = QCheckBox("Thiết bị bị hỏng")
        self.quality_combo.currentIndexChanged.connect(self.on_quality_change)

        # Checkbox for return date today
        self.return_date_today = QCheckBox("Trả thiết bị ngày hôm nay")
        self.return_date_today.setChecked(True)

        # Container for label + calendar
        self.return_date_container = QWidget()
        return_date_layout = QHBoxLayout(self.return_date_container)
        return_date_layout.setContentsMargins(0, 0, 0, 0)

        self.return_date_label = QLabel("Ngày Trả Thực Tế:")
        self.actual_return_date_edit = QDateEdit()
        self.actual_return_date_edit.setCalendarPopup(True)
        self.actual_return_date_edit.setDate(QDate.currentDate())

        return_date_layout.addWidget(self.return_date_label)
        return_date_layout.addWidget(self.actual_return_date_edit)

        self.return_date_container.hide()
        self.return_date_today.toggled.connect(self.on_return_date_toggle)

        layout.addRow("Chọn Chất Lượng Trả:", self.quality_combo)
        layout.addRow("", self.check_broken)
        layout.addRow(self.return_date_today)
        layout.addRow(self.return_date_container)
        
        # Buttons
        btn_box = QHBoxLayout()
        btn_ok = QPushButton("Xác Nhận")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_ok)
        btn_box.addWidget(btn_cancel)
        layout.addRow(btn_box)

        self.setLayout(layout)

    def on_quality_change(self, index):
        quality = self.quality_combo.itemData(index)
        if quality == DeviceQualityStatus.BROKEN:
            self.check_broken.setChecked(True)
        else:
            self.check_broken.setChecked(False)

    def on_return_date_toggle(self, checked: bool):
        if checked:
            self.return_date_container.hide()
        else:
            self.return_date_container.show()

    def get_data(self):
        return {
            "return_quality_status": self.quality_combo.currentData(),
            "broken_status": self.check_broken.isChecked(),
            "actual_return_date": self.actual_return_date_edit.date().toString("yyyy-MM-dd") if not self.return_date_today.isChecked() else datetime.now().strftime("%Y-%m-%d")
        }