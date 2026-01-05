from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHeaderView, QAbstractItemView, QMessageBox, 
    QDialog, QFormLayout, QLineEdit, QTabWidget, QComboBox
)

from PyQt6.QtCore import Qt, pyqtSignal


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

# === Sub-Tab Departments ===
class DepartmentsSubTab(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, hr_manager):
        super().__init__()
        self.hr_manager = hr_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # === Toolbar ===
        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("🔄 Làm mới")
        self.btn_load.clicked.connect(self.load_data)

        self.btn_add = QPushButton("➕ Thêm phòng ban")
        self.btn_add.clicked.connect(self.open_add_department_dialog)

        self.btn_delete = QPushButton("🗑️ Xóa phòng ban")
        self.btn_delete.clicked.connect(self.delete_selected_department)

        self.btn_add.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_delete.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")

        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # === Table ===
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên", "Quản lý", "Địa điểm"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()
    
    def load_data(self):
        try:
            departments = self.hr_manager.get_all_departments()
            self.table.setRowCount(0)
            for row, dept in enumerate(departments):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(dept.get_id()))
                self.table.setItem(row, 1, QTableWidgetItem(dept.get_name()))
                self.table.setItem(row, 2, QTableWidgetItem(dept.get_manager().name if dept.get_manager() else "Không có"))
                self.table.setItem(row, 3, QTableWidgetItem(dept.get_location()))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu phòng ban:\n{str(e)}")

    def open_add_department_dialog(self):
        dialog = AddDepartmentDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.hr_manager.create_and_add_department(
                    name=data['name'],
                    location=data['location'],
                )
                self.load_data()
                self.data_changed.emit()
                QMessageBox.information(self, "Thành công", "Đã thêm phòng ban!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể thêm: {e}")          

    def delete_selected_department(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Chú ý", "Vui lòng chọn một phòng ban để xóa.")
            return
        dept_id = self.table.item(current_row, 0).text()

        confirm = QMessageBox.question(self, "Xác nhận",
            f"Bạn có chắc chắn muốn xóa phòng ban ID {dept_id} không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.hr_manager.remove_department(dept_id)
            QMessageBox.information(self, "Thành công", "Đã xóa phòng ban!")
            self.load_data()
            self.data_changed.emit()    

# === Sub-Tab Employees ===
class EmployeesSubTab(QWidget):
    def __init__(self, hr_manager):
        super().__init__()
        self.hr_manager = hr_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # === Toolbar ===
        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("🔄 Làm mới")
        self.btn_load.clicked.connect(self.load_data)
        self.btn_add = QPushButton("➕ Thêm nhân viên")
        self.btn_add.clicked.connect(self.open_add_employee_dialog)
        self.btn_delete = QPushButton("🗑️ Xóa nhân viên")
        self.btn_delete.clicked.connect(self.delete_selected_employee)

        self.btn_add.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_delete.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")

        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # === Table ===
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên", "Email", "Số điện thoại", "Chức vụ", "Phòng ban"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        self.department_cache = [] # Cache phòng ban để chọn khi thêm nhân viên

        self.setLayout(layout)
        self.load_data()
        self.load_departments_combobox()

    def load_data(self):
        try:
            employees = self.hr_manager.get_all_employees()
            self.table.setRowCount(0)
            for row, emp in enumerate(employees):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(emp.get_id()))
                self.table.setItem(row, 1, QTableWidgetItem(emp.name))
                self.table.setItem(row, 2, QTableWidgetItem(emp.email))
                self.table.setItem(row, 3, QTableWidgetItem(emp.phone_number))
                self.table.setItem(row, 4, QTableWidgetItem(emp.get_position()))
                self.table.setItem(row, 5, QTableWidgetItem(emp.get_department().get_name() if emp.get_department() else "Không có"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu nhân viên:\n{str(e)}")

    def load_departments_combobox(self):
        try:
            self.department_cache = self.hr_manager.get_all_departments()
        except Exception as e:
            self.department_cache = []

    def open_add_employee_dialog(self):
        dialog = AddEmployeeDialog(self, self.department_cache)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.hr_manager.create_and_add_employee(
                    name=data['name'],
                    email=data['email'],
                    phone_number=data['phone_number'],
                    position=data['position'],
                    department_id = data['department_id']
                )
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã thêm nhân viên!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể thêm: {e}")

    def delete_selected_employee(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Chú ý", "Vui lòng chọn một nhân viên để xóa.")
            return
        emp_id = self.table.item(current_row, 0).text()

        if QMessageBox.question(self, "Xác nhận",
            f"Bạn có chắc chắn muốn xóa nhân viên ID {emp_id} không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.hr_manager.remove_employee(emp_id)
            QMessageBox.information(self, "Thành công", "Đã xóa nhân viên!")
            self.load_data()
    
# === Dialogs ===

class AddDepartmentDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Phòng Ban Mới")
        self.setFixedSize(350, 250)
        layout = QFormLayout()

        self.name = QLineEdit()
        self.location = QLineEdit()

        layout.addRow("Tên Phòng Ban:", self.name)
        layout.addRow("Địa Điểm:", self.location)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.accept)
        btn_box.addWidget(btn_save)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_cancel)

        layout.addRow(btn_box)
        self.setLayout(layout)

    def get_data(self):
        return {
            "name": self.name.text(),
            "location": self.location.text()
        }
    
class AddEmployeeDialog(QDialog):
    def __init__(self, parent = None, departments = None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Nhân Viên Mới")
        self.setFixedSize(350, 250)
        layout = QFormLayout()

        self.name = QLineEdit()
        self.email = QLineEdit()
        self.phone_number = QLineEdit()
        self.position = QLineEdit()
        self.department_combo = QComboBox()

        self.departments = departments if departments else []

        if departments:
            for dept in departments:
                self.department_combo.addItem(dept.get_name())

        layout.addRow("Tên Nhân Viên:", self.name)
        layout.addRow("Email:", self.email)
        layout.addRow("Số Điện Thoại:", self.phone_number)
        layout.addRow("Chức Vụ:", self.position)
        layout.addRow("Phòng Ban:", self.department_combo)

        btn_box = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.accept)
        btn_box.addWidget(btn_save)
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(btn_cancel)
        layout.addRow(btn_box)
        self.setLayout(layout)

    def get_data(self):

        current_index = self.department_combo.currentIndex()
        department_id = self.departments[current_index].get_id() if current_index >=0 and self.departments else None

        return {
            "name": self.name.text(),
            "email": self.email.text(),
            "phone_number": self.phone_number.text(),
            "position": self.position.text(),
            "department_id": department_id
        }