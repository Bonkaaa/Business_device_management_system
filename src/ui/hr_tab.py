from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHeaderView, QAbstractItemView, QMessageBox, 
    QDialog, QFormLayout, QLineEdit, QTabWidget, QComboBox, QLabel, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QBrush

from utils.constant_class import DeviceQualityStatus, DeviceStatus
from utils.validators import DepartmentValidator, EmployeeValidator

# === 1. Popup Chi tiết Nhân viên ===
class EmployeeDetailDialog(QDialog):
    def __init__(self, employee, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Chi tiết nhân viên - {employee.name}")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        group = QGroupBox("Thông tin cá nhân")
        form = QFormLayout()
        form.addRow("<b>ID:</b>", QLabel(employee.get_id()))
        form.addRow("<b>Họ tên:</b>", QLabel(employee.name))
        form.addRow("<b>Email:</b>", QLabel(employee.email))
        form.addRow("<b>Số điện thoại:</b>", QLabel(employee.phone_number))
        form.addRow("<b>Chức vụ:</b>", QLabel(employee.get_position()))
        form.addRow("<b>Phòng ban:</b>", QLabel(employee.get_department().get_name() if employee.get_department() else "N/A"))
        form.addRow("<b>Thiết bị được giao:</b>", QLabel(", ".join(employee.get_assigned_devices()) if employee.get_assigned_devices() else "Chưa có"))
        
        group.setLayout(form)
        layout.addWidget(group)
        
        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

# === 2. Popup Chi tiết Phòng ban ===
class DepartmentDetailDialog(QDialog):
    def __init__(self, dept, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Chi tiết phòng ban - {dept.get_name()}")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        group = QGroupBox("Thông tin phòng ban")
        form = QFormLayout()
        
        form.addRow("<b>ID Phòng:</b>", QLabel(dept.get_id()))
        form.addRow("<b>Tên phòng:</b>", QLabel(dept.get_name()))
        form.addRow("<b>Địa điểm:</b>", QLabel(dept.get_location()))
        form.addRow("<b>Quản lý:</b>", QLabel(dept.get_manager().name if dept.get_manager() else "Chưa có"))
        form.addRow("<b>Nhân viên:</b>", QLabel(", ".join([emp.name for emp in dept.get_employees()]) if dept.get_employees() else "Chưa có"))
        form.addRow("<b>Thiết bị được giao:</b>", QLabel(", ".join(dept.get_assigned_devices()) if dept.get_assigned_devices() else "Chưa có"))
        
        group.setLayout(form)
        layout.addWidget(group)
        
        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

# === 3. Sub-Tab Employees (Đã nâng cấp) ===
class EmployeesSubTab(QWidget):
    def __init__(self, hr_manager):
        super().__init__()
        self.hr_manager = hr_manager
        self.all_employees = []
        self.department_cache = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Toolbar
        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("🔄 Làm mới")
        self.btn_add = QPushButton("➕ Thêm nhân viên")
        self.btn_delete = QPushButton("🗑️ Xóa")
        
        self.btn_add.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_delete.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        self.btn_load.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.open_add_employee_dialog)
        self.btn_delete.clicked.connect(self.delete_selected_employee)

        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Filter Bar
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm theo ID, Tên, Email...")
        self.search_input.textChanged.connect(self.apply_filters)
        
        self.combo_dept = QComboBox()
        self.combo_dept.currentTextChanged.connect(self.apply_filters)

        filter_layout.addWidget(QLabel("Tìm kiếm:"))
        filter_layout.addWidget(self.search_input, 3)
        filter_layout.addWidget(QLabel("Phòng ban:"))
        filter_layout.addWidget(self.combo_dept, 2)
        layout.addLayout(filter_layout)

        # Table (Làm gọn còn 4 cột)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Họ Tên", "Chức vụ", "Phòng ban"])
        
        # UI Table
        font = QFont()
        font.setPointSize(11)
        self.table.setFont(font)
        self.table.verticalHeader().setDefaultSectionSize(35)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.show_employee_details)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet("font-weight: bold;")
        
        layout.addWidget(self.table)
        layout.addWidget(QLabel("<i>* Nhấp đúp vào một dòng để xem chi tiết đầy đủ của thiết bị.</i>"))
        self.setLayout(layout)
        
        self.load_data()

    def load_data(self):
        try:
            self.all_employees = self.hr_manager.get_all_employees()
            self.load_departments_combobox()
            self.apply_filters()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def load_departments_combobox(self):
        self.department_cache = self.hr_manager.get_all_departments()
        self.combo_dept.blockSignals(True)
        self.combo_dept.clear()
        self.combo_dept.addItem("-- Tất cả --")
        for dept in self.department_cache:
            self.combo_dept.addItem(dept.get_name())
        self.combo_dept.blockSignals(False)

    def apply_filters(self):
        search_text = self.search_input.text().lower()
        dept_filter = self.combo_dept.currentText()
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        for emp in self.all_employees:
            dept_name = emp.get_department().get_name() if emp.get_department() else "Không có"
            
            match_search = (search_text in emp.get_id().lower() or 
                            search_text in emp.name.lower() or 
                            search_text in emp.email.lower())
            match_dept = (dept_filter == "-- Tất cả --" or dept_filter == dept_name)
            
            if match_search and match_dept:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(emp.get_id()))
                self.table.setItem(row, 1, QTableWidgetItem(emp.name))
                self.table.setItem(row, 2, QTableWidgetItem(emp.get_position()))
                self.table.setItem(row, 3, QTableWidgetItem(dept_name))
        
        self.table.setSortingEnabled(True)

    def show_employee_details(self, row, col):
        emp_id = self.table.item(row, 0).text()
        emp = next((e for e in self.all_employees if e.get_id() == emp_id), None)
        if emp:
            EmployeeDetailDialog(emp, self).exec()

    # (Các hàm open_add_employee_dialog và delete giữ nguyên logic cũ của bạn)
    def open_add_employee_dialog(self):
        dialog = AddEmployeeDialog(self, self.department_cache)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.hr_manager.create_and_add_employee(
                    name=data['name'], email=data['email'],
                    phone_number=data['phone_number'], position=data['position'],
                    department_id=data['department_id']
                )
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def delete_selected_employee(self):
        row = self.table.currentRow()
        if row < 0: 
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một nhân viên để xóa.")
            return
        emp_id = self.table.item(row, 0).text()
        if QMessageBox.question(self, "Xác nhận", f"Xóa nhân viên {emp_id}?") == QMessageBox.StandardButton.Yes:

            # Remove employee from department's employee list
            emp = self.hr_manager.get_employee_by_id(emp_id, fetch_dept=True)
            if emp and emp.get_department():
                self.hr_manager.remove_employee_from_department_employee_list(emp_id, emp.get_department().get_id())
            else:
                QMessageBox.warning(self, "Cảnh báo", "Không thể cập nhật danh sách nhân viên của phòng ban do không tìm thấy phòng ban.")

            # Change assigned devices' status to 'available'
            assigned_devices = emp.get_assigned_devices() if emp else []
            for device_str in assigned_devices:
                device_id = device_str.split("-")[0]
                self.hr_manager.inventory_manager.update_device_status_and_assignee(
                    device_id=device_id,
                    new_status=DeviceStatus.AVAILABLE,
                    new_assignee_id=None
                )
            
            # Close active assignments related to this employee
            assignments = self.hr_manager.assignment_manager.get_active_assignment_by_assignee_id(emp_id)
            if assignments:
                for assignment in assignments:
                    self.hr_manager.assignment_manager.close_assignment(
                        assignment_id=assignment.get_id(),
                        return_quality_status=DeviceQualityStatus.GOOD,
                        actual_return_date=datetime.now().isoformat(),
                        broken_status=False
                    )

            # Finally, remove employee from database
            self.hr_manager.remove_employee(emp_id)
            self.load_data()


# === 4. Sub-Tab Departments (Đã nâng cấp) ===
class DepartmentsSubTab(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, hr_manager):
        super().__init__()
        self.hr_manager = hr_manager
        self.all_depts = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Toolbar
        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("🔄 Làm mới")
        self.btn_add = QPushButton("➕ Thêm phòng ban")
        self.btn_delete = QPushButton("🗑️ Xóa")
        self.btn_add_manager = QPushButton("👤 Chỉ định quản lý")
        
        self.btn_add.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_delete.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.btn_add_manager.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")

        self.btn_load.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.open_add_department_dialog)
        self.btn_delete.clicked.connect(self.delete_selected_department)
        self.btn_add_manager.clicked.connect(self.open_assign_manager_dialog)


        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_add_manager)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm phòng ban theo ID, Tên, Quản lý...")
        self.search_input.textChanged.connect(self.apply_filters)
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table (Làm gọn 4 cột)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Tên Phòng", "Quản lý", "Địa điểm"])
        
        font = QFont()
        font.setPointSize(11)
        self.table.setFont(font)
        self.table.verticalHeader().setDefaultSectionSize(35)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.show_dept_details)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet("font-weight: bold;")

        layout.addWidget(self.table)
        layout.addWidget(QLabel("<i>* Nhấp đúp vào một dòng để xem chi tiết đầy đủ của thiết bị.</i>"))

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            self.all_depts = self.hr_manager.get_all_departments()
            self.apply_filters()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def apply_filters(self):
        search_text = self.search_input.text().lower()
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        for dept in self.all_depts:
            mgr_name = dept.get_manager().name if dept.get_manager() else "Không có"
            
            if (search_text in dept.get_id().lower() or 
                search_text in dept.get_name().lower() or 
                search_text in mgr_name.lower()):
                
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(dept.get_id()))
                self.table.setItem(row, 1, QTableWidgetItem(dept.get_name()))
                self.table.setItem(row, 2, QTableWidgetItem(mgr_name))
                self.table.setItem(row, 3, QTableWidgetItem(dept.get_location()))
        
        self.table.setSortingEnabled(True)

    def show_dept_details(self, row, col):
        dept_id = self.table.item(row, 0).text()
        dept = next((d for d in self.all_depts if d.get_id() == dept_id), None)
        if dept:
            DepartmentDetailDialog(dept, self).exec()

    def open_add_department_dialog(self):
        dialog = AddDepartmentDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.hr_manager.create_and_add_department(name=data['name'], location=data['location'])
                self.load_data()
                self.data_changed.emit()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def delete_selected_department(self):
        row = self.table.currentRow()
        if row < 0: 
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một phòng ban để xóa.")
            return
        dept_id = self.table.item(row, 0).text()
        if QMessageBox.question(self, "Xác nhận", f"Xóa phòng {dept_id}?") == QMessageBox.StandardButton.Yes:
            
            # Remove department from employees in this department
            employees = self.hr_manager.get_employees_by_department_id(dept_id)
            for emp in employees:
                self.hr_manager.set_none_department_to_employee(emp.get_id())
            
            # Change assigned devices' status to 'available'
            dept = self.hr_manager.get_department_by_id(dept_id)
            assigned_devices = dept.get_assigned_devices() if dept else []
            for device_str in assigned_devices:
                device_id = device_str.split("-")[0]
                self.hr_manager.inventory_manager.update_device_status_and_assignee(
                    device_id=device_id,
                    new_status=DeviceStatus.AVAILABLE,
                    new_assignee_id=None
                )
            
            # Close active assignments related to this department
            assignments = self.hr_manager.assignment_manager.get_active_assignment_by_assignee_id(dept_id)
            if assignments:
                for assignment in assignments:
                    self.hr_manager.assignment_manager.close_assignment(
                        assignment_id=assignment.get_id(),
                        return_quality_status=DeviceQualityStatus.GOOD,
                        actual_return_date=datetime.now().isoformat(),
                        broken_status=False
                    )
 
            # Finally, remove department from database
            self.hr_manager.remove_department(dept_id)
            self.load_data()
            self.data_changed.emit()

    def open_assign_manager_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một nhân viên để chỉ định làm quản lý.")
            return

        department_id = self.table.item(row, 0).text()
        department = self.hr_manager.get_department_by_id(department_id)
        if not department:
            QMessageBox.critical(self, "Lỗi", "Phòng ban không tồn tại.")
            return
        
        dialog = AssignManagerDialog(department, self, employees=self.hr_manager.get_all_employees())
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.hr_manager.assign_manager_to_department(
                    department_id=department_id,
                    manager_employee_id=data['employee_id']
                )
                self.load_data()
                self.data_changed.emit()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

# === (Giữ nguyên các class HRTab, AddDepartmentDialog, AddEmployeeDialog của bạn) ===
class HRTab(QWidget):
    def __init__(self, hr_manager):
        super().__init__()
        self.hr_manager = hr_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.sub_tabs = QTabWidget()
        self.employees_tab = EmployeesSubTab(self.hr_manager)
        self.departments_tab = DepartmentsSubTab(self.hr_manager)
        self.departments_tab.data_changed.connect(self.employees_tab.load_departments_combobox)
        self.sub_tabs.addTab(self.employees_tab, "👥 Nhân Viên")
        self.sub_tabs.addTab(self.departments_tab, "🏢 Phòng Ban")
        layout.addWidget(self.sub_tabs)
        self.setLayout(layout)

class AddDepartmentDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Phòng Ban Mới")
        self.setFixedSize(350, 200)
        layout = QFormLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Tên phòng ban")

        self.location = QLineEdit()
        self.location.setPlaceholderText("Địa điểm phòng ban")

        layout.addRow("Tên Phòng Ban:", self.name)
        layout.addRow("Địa Điểm:", self.location)
        btn_box = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.handle_save)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_save); btn_box.addWidget(btn_cancel)
        layout.addRow(btn_box)
        self.setLayout(layout)

    def get_data(self):
        return {"name": self.name.text(), "location": self.location.text()}
    
    def handle_save(self):
        name = self.name.text().strip()
        location = self.location.text().strip()

        valid_name = DepartmentValidator.validate_department_input(
            name=name,
            location=location
        )

        if valid_name is not True:
            QMessageBox.warning(self, "Lỗi", valid_name)
            return

        self.accept()

class AddEmployeeDialog(QDialog):
    def __init__(self, parent = None, departments = None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Nhân Viên Mới")
        self.setFixedSize(350, 200)
        layout = QFormLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Họ và tên đầy đủ")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Ví dụ: abc@gmail.com")

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Ví dụ: 0123456789")

        self.position = QLineEdit()
        self.position.setPlaceholderText("Chức vụ trong công ty")

        self.department_combo = QComboBox()
        self.departments = departments if departments else []
        for dept in self.departments: self.department_combo.addItem(dept.get_name())
        layout.addRow("Họ Tên:", self.name)
        layout.addRow("Email:", self.email)
        layout.addRow("SĐT:", self.phone_number)
        layout.addRow("Chức Vụ:", self.position)
        layout.addRow("Phòng Ban:", self.department_combo)
        btn_box = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.handle_save)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_save); btn_box.addWidget(btn_cancel)
        layout.addRow(btn_box)
        self.setLayout(layout)

    def get_data(self):
        idx = self.department_combo.currentIndex()
        return {
            "name": self.name.text(), "email": self.email.text(),
            "phone_number": self.phone_number.text(), "position": self.position.text(),
            "department_id": self.departments[idx].get_id() if idx >=0 else None
        }
    
    def handle_save(self):
        name = self.name.text().strip()
        email = self.email.text().strip()
        phone = self.phone_number.text().strip()
        position = self.position.text().strip()

        valid = EmployeeValidator.validate_employee_input(
            name=name,
            email=email,
            phone=phone,
            position=position
        )

        if valid is not True:
            QMessageBox.warning(self, "Lỗi", valid)
            return

        self.accept()
    
class AssignManagerDialog(QDialog):
    def __init__(self, department, parent=None, employees=None):
        super().__init__(parent)
        self.setWindowTitle("Chỉ Định Quản Lý Phòng Ban")
        self.setFixedSize(400, 200)
        layout = QFormLayout()
        
        self.department = department
        self.employees = employees if employees else []
        
        self.emp_combo = QComboBox()
        for emp in self.employees:
            self.emp_combo.addItem(emp.name)
        
        layout.addRow("Chọn Nhân Viên làm Quản Lý:", self.emp_combo)
        
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
        emp_idx = self.emp_combo.currentIndex()

        return {
            "employee_id": self.employees[emp_idx].get_id() if emp_idx >= 0 else None
        }