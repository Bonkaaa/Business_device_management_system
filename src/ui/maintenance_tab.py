from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHeaderView, QAbstractItemView, QMessageBox, 
    QDialog, QFormLayout, QComboBox, QTextEdit, QSpinBox, QCheckBox, QLabel, QGroupBox, QLineEdit
)
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QColor, QBrush, QFont
from src.utils.constant_class import MaintenanceStatus, DeviceStatus, UserRole

# === 1. Popup Chi tiết Phiếu Bảo Trì ===
class MaintenanceDetailDialog(QDialog):
    def __init__(self, ticket, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Chi tiết bảo trì - {ticket.get_id()}")
        self.setMinimumWidth(450)
        self.init_ui(ticket)

    def init_ui(self, t):
        layout = QVBoxLayout()
        
        # Group 1: Thông tin chung
        group_info = QGroupBox("Thông tin phiếu")
        form = QFormLayout()
        
        dev_name = t.get_device().name if t.get_device() else "N/A"
        rep_name = t.get_reporter().name if t.get_reporter() else "N/A"
        status_str = t.get_status().value if hasattr(t.get_status(), 'value') else str(t.get_status())
        date_str = t.get_reported_date().strftime("%d/%m/%Y %H:%M")

        form.addRow("<b>Mã phiếu:</b>", QLabel(t.get_id()))
        form.addRow("<b>Thiết bị:</b>", QLabel(dev_name))
        form.addRow("<b>Người báo cáo:</b>", QLabel(rep_name))
        form.addRow("<b>Ngày báo hỏng:</b>", QLabel(date_str))
        form.addRow("<b>Trạng thái:</b>", QLabel(status_str))
        
        group_info.setLayout(form)
        layout.addWidget(group_info)

        # Group 2: Mô tả & Xử lý
        group_desc = QGroupBox("Nội dung xử lý")
        desc_layout = QVBoxLayout()
        
        desc_text = f"<b>Mô tả lỗi:</b><br>{t.get_issue_description()}<br><br>"
        notes = t.get_technician_notes() if hasattr(t, 'get_technician_notes') else "Chưa có ghi chú xử lý."
        desc_text += f"<b>Ghi chú kỹ thuật:</b><br>{notes if notes else '...'}<br><br>"
        
        cost = t.get_costs() if t.get_costs() else 0
        desc_text += f"<b>Chi phí sửa chữa:</b> {cost:,.0f} VND"
        
        label_desc = QLabel(desc_text)
        label_desc.setWordWrap(True)
        desc_layout.addWidget(label_desc)
        group_desc.setLayout(desc_layout)
        layout.addWidget(group_desc)

        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

# === 2. Tab Maintenance Chính ===
class MaintenanceTab(QWidget):
    def __init__(self, maintenance_manager, inventory_manager, hr_manager, current_user):
        super().__init__()
        self.maintenance_manager = maintenance_manager
        self.inventory_manager = inventory_manager
        self.hr_manager = hr_manager
        self.current_user = current_user
        self.all_tickets = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        # === Toolbar ===
        toolbar = QHBoxLayout()
        self.btn_load = QPushButton("🔄 Làm mới")
        self.btn_report = QPushButton("📝 Báo hỏng")
        self.btn_resolve = QPushButton("🛠️ Cập nhật xử lý")
        self.btn_close_ticket = QPushButton("✅ Đóng phiếu")

        self.btn_report.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px 12px;")
        self.btn_resolve.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 5px 12px;")
        self.btn_close_ticket.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 5px 12px;")

        toolbar.addWidget(self.btn_load)
        toolbar.addWidget(self.btn_report)
        toolbar.addWidget(self.btn_resolve)
        toolbar.addWidget(self.btn_close_ticket)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # === Filter Bar ===
        filter_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm theo Mã phiếu, Tên thiết bị, Người báo...")
        self.search_input.setFixedHeight(30)
        self.search_input.textChanged.connect(self.apply_filters)

        self.combo_status = QComboBox()
        self.combo_status.setFixedHeight(30)
        self.combo_status.addItems(["-- Tất cả trạng thái --", 
                                   MaintenanceStatus.REPORTED.value, 
                                   MaintenanceStatus.RESOLVED.value, 
                                   MaintenanceStatus.CLOSED.value])
        self.combo_status.currentTextChanged.connect(self.apply_filters)

        filter_bar.addWidget(QLabel("Tìm kiếm:"))
        filter_bar.addWidget(self.search_input, 3)
        filter_bar.addWidget(QLabel("Lọc:"))
        filter_bar.addWidget(self.combo_status, 1)
        layout.addLayout(filter_bar)

        # === Table (Đã làm gọn còn 4 cột) ===
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Mã Phiếu", "Thiết Bị", "Trạng Thái", "Ngày Báo"])
        
        font = QFont()
        font.setPointSize(10)
        self.table.setFont(font)
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # Kết nối sự kiện
        self.btn_load.clicked.connect(self.load_data)
        self.btn_report.clicked.connect(self.open_report_dialog)
        self.btn_resolve.clicked.connect(self.open_resolve_dialog)
        self.btn_close_ticket.clicked.connect(self.open_close_dialog)
        self.table.cellDoubleClicked.connect(self.show_detail)

        layout.addWidget(self.table)
        layout.addWidget(QLabel("<i>* Nhấp đúp vào dòng để xem chi tiết mô tả sự cố và chi phí xử lý.</i>"))
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            if self.current_user['role'] == UserRole.EMPLOYEE.value:
                emp_id = self.current_user.get('employee_id', None)
                if emp_id:
                    self.all_tickets = self.maintenance_manager.get_tickets_by_reporter_id(emp_id)
                else:
                    self.all_tickets = []
            else:
                self.all_tickets = self.maintenance_manager.get_all_tickets()
            self.apply_filters()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {e}")

    def apply_filters(self):
        search_text = self.search_input.text().lower()
        status_filter = self.combo_status.currentText()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for ticket in self.all_tickets:
            t_id = ticket.get_id().lower()
            dev_name = ticket.get_device().name.lower() if ticket.get_device() else ""
            rep_name = ticket.get_reporter().name.lower() if ticket.get_reporter() else ""
            
            status_val = ticket.get_status()
            status_str = status_val.value if hasattr(status_val, 'value') else str(status_val)

            match_search = (search_text in t_id or search_text in dev_name or search_text in rep_name)
            match_status = (status_filter == "-- Tất cả trạng thái --" or status_filter == status_str)

            if match_search and match_status:
                self.add_row(ticket, status_str)

        self.table.setSortingEnabled(True)

    def add_row(self, ticket, status_str):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(ticket.get_id()))
        self.table.setItem(row, 1, QTableWidgetItem(ticket.get_device().name if ticket.get_device() else "N/A"))
        
        item_status = QTableWidgetItem(status_str)
        # Luôn để chữ màu đen
        item_status.setForeground(QBrush(QColor(0, 0, 0)))

        if status_str == MaintenanceStatus.REPORTED.value:
            # Đỏ nhạt – cảnh báo
            item_status.setBackground(QBrush(QColor("#FFCDD2")))
            
        elif status_str == MaintenanceStatus.RESOLVED.value:
            # Cam nhạt – đang xử lý
            item_status.setBackground(QBrush(QColor("#FFE0B2")))
            
        elif status_str == MaintenanceStatus.CLOSED.value:
            # Xám nhạt – đã xong
            item_status.setBackground(QBrush(QColor("#E0E0E0")))
            
        self.table.setItem(row, 2, item_status)
        
        date_str = ticket.get_reported_date().strftime("%d/%m/%Y")
        self.table.setItem(row, 3, QTableWidgetItem(date_str))

    def show_detail(self, row, col):
        t_id = self.table.item(row, 0).text()
        ticket = next((t for t in self.all_tickets if t.get_id() == t_id), None)
        if ticket:
            MaintenanceDetailDialog(ticket, self).exec()

    # --- Các hàm logic giữ nguyên từ bản của bạn nhưng sửa lỗi gọi thuộc tính ---

    def open_report_dialog(self):
        all_devs = self.inventory_manager.get_all_devices()
        valid_devs = [d for d in all_devs if d.get_status()["status"] != DeviceStatus.MAINTENANCE]
        employees = self.hr_manager.get_all_employees()

        dialog = ReportIssueDialog(valid_devs, employees, self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.maintenance_manager.create_ticket(
                    issue_description=data['description'],
                    device=data['device'],
                    reporter=data['reporter']
                )
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã báo hỏng thiết bị.")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def open_resolve_dialog(self):
        row = self.table.currentRow()
        if row < 0: 
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một phiếu để cập nhật.")
            return
        ticket_id = self.table.item(row, 0).text()
        status_text = self.table.item(row, 2).text()
        
        if status_text == MaintenanceStatus.CLOSED.value:
            QMessageBox.warning(self, "Lỗi", "Phiếu đã đóng không thể sửa.")
            return

        dialog = ResolveTicketDialog(ticket_id, self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.maintenance_manager.resolve_ticket(
                    ticket_id=ticket_id,
                    technician_notes=data['notes'],
                    costs=data['cost']
                )
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def open_close_dialog(self):
        row = self.table.currentRow()
        if row < 0: 
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một phiếu để đóng.")
            return
        ticket_id = self.table.item(row, 0).text()
        if self.table.item(row, 2).text() == MaintenanceStatus.CLOSED.value: return

        dialog = CloseTicketDialog(ticket_id, self)
        if dialog.exec():
            is_repaired = dialog.get_result()
            try:
                self.maintenance_manager.close_ticket(ticket_id=ticket_id, is_repaired=is_repaired)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

# === Các Dialogs của bạn (Giữ nguyên logic chính) ===
class ReportIssueDialog(QDialog):
    def __init__(self, devices, employees, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Báo hỏng thiết bị")
        self.setFixedSize(400, 300)
        layout = QFormLayout()
        self.cmb_device = QComboBox()
        for dev in devices: self.cmb_device.addItem(f"{dev.name} ({dev.get_id()})", dev)
        self.cmb_reporter = QComboBox()
        for emp in employees: self.cmb_reporter.addItem(f"{emp.name} ({emp.get_id()})", emp)
        self.txt_description = QTextEdit()
        layout.addRow("Thiết Bị:", self.cmb_device)
        layout.addRow("Người Báo:", self.cmb_reporter)
        layout.addRow("Mô Tả Lỗi:", self.txt_description)
        btn_ok = QPushButton("Gửi báo cáo"); btn_ok.clicked.connect(self.accept)
        layout.addRow(btn_ok)
        self.setLayout(layout)
    def get_data(self):
        return {'device': self.cmb_device.currentData(), 'reporter': self.cmb_reporter.currentData(), 'description': self.txt_description.toPlainText().strip()}

class ResolveTicketDialog(QDialog):
    def __init__(self, ticket_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Xử lý {ticket_id}")
        layout = QFormLayout()
        self.txt_notes = QTextEdit()

        self.spn_cost = QSpinBox()
        self.spn_cost.setRange(0, 1_000_000_000)
        self.spn_cost.setSingleStep(50_000)
        self.spn_cost.setSuffix(" VND")

        # Quan trọng: bật định dạng có dấu phân cách 100.000
        locale = QLocale(QLocale.Language.Vietnamese, QLocale.Country.Vietnam)
        self.spn_cost.setLocale(locale)
        self.spn_cost.setGroupSeparatorShown(True)

        layout.addRow("Ghi chú:", self.txt_notes)
        layout.addRow("Chi phí:", self.spn_cost)
        btn = QPushButton("Cập nhật"); btn.clicked.connect(self.accept)
        layout.addRow(btn)
        self.setLayout(layout)
    def get_data(self):
        return {'notes': self.txt_notes.toPlainText().strip(), 'cost': self.spn_cost.value()}

class CloseTicketDialog(QDialog):
    def __init__(self, ticket_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đóng phiếu")
        layout = QVBoxLayout()
        self.chk_repaired = QCheckBox("Thiết bị đã sửa tốt")
        self.chk_repaired.setChecked(True)
        btn = QPushButton("Xác nhận đóng"); btn.clicked.connect(self.accept)
        layout.addWidget(QLabel(f"Xác nhận kết quả bảo trì phiếu {ticket_id}:"))
        layout.addWidget(self.chk_repaired)
        layout.addWidget(btn)
        self.setLayout(layout)
    def get_result(self): 
        return self.chk_repaired.isChecked()