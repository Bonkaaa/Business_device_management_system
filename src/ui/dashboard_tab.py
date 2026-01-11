# File: src/ui/dashboard_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import các hằng số trạng thái
from utils.constant_class import DeviceQualityStatus, MaintenanceStatus

class StatCard(QFrame):
    """Widget hiển thị một thẻ thống kê (Card)"""
    def __init__(self, title, value, icon_text, color_code):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(120)
        # Sửa CSS để card bo tròn đẹp hơn và text dễ đọc
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color_code};
                border-radius: 12px;
                color: white;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10) # Padding trong card
        
        # Hàng 1: Icon bên phải
        icon_layout = QHBoxLayout()
        icon_layout.addStretch()
        lbl_icon = QLabel(icon_text)
        lbl_icon.setFont(QFont("Segoe UI", 24))
        lbl_icon.setStyleSheet("background: transparent; border: none;")
        icon_layout.addWidget(lbl_icon)
        layout.addLayout(icon_layout)
        
        # Hàng 2: Số liệu to
        self.lbl_value = QLabel(str(value))
        self.lbl_value.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        self.lbl_value.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(self.lbl_value)
        
        # Hàng 3: Tiêu đề nhỏ
        lbl_title = QLabel(title)
        lbl_title.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        lbl_title.setStyleSheet("background: transparent; border: none; opacity: 0.9;")
        layout.addWidget(lbl_title)
        
        self.setLayout(layout)

    def update_value(self, new_value):
        self.lbl_value.setText(str(new_value))

class DashboardTab(QWidget):
    def __init__(self, inventory_mgr, hr_mgr, assignment_mgr, maintenance_mgr):
        super().__init__()
        self.inventory_mgr = inventory_mgr
        self.hr_mgr = hr_mgr
        self.assignment_mgr = assignment_mgr
        self.maintenance_mgr = maintenance_mgr

        self.init_ui()

    def init_ui(self):
        # Setup ScrollArea để cuộn nếu màn hình bé
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        # Quan trọng: Set style cho ScrollArea trong suốt để hợp với nền tối
        scroll.setStyleSheet("QScrollArea { background: transparent; } QWidget { background: transparent; }")
        
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(20, 20, 20, 40)
        main_layout.setSpacing(25) # Tăng khoảng cách giữa các phần

        # --- 1. Header ---
        lbl_header = QLabel("TỔNG QUAN HỆ THỐNG")
        # Đổi màu chữ sang xám nhạt (#eee) để nhìn rõ trên nền tối
        lbl_header.setStyleSheet("color: #eee;") 
        lbl_header.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        main_layout.addWidget(lbl_header)

        # --- 2. Hàng Thẻ thống kê (Top Cards) ---
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.card_total_devices = StatCard("Tổng thiết bị", 0, "🖥️", "#2196F3") # Blue
        cards_layout.addWidget(self.card_total_devices)

        self.card_assigned = StatCard("Đang sử dụng", 0, "👤", "#4CAF50") # Green
        cards_layout.addWidget(self.card_assigned)

        self.card_maintenance = StatCard("Đang bảo trì/Hỏng", 0, "🛠️", "#F44336") # Red
        cards_layout.addWidget(self.card_maintenance)

        self.card_employees = StatCard("Tổng nhân sự", 0, "👥", "#FF9800") # Orange
        cards_layout.addWidget(self.card_employees)

        main_layout.addLayout(cards_layout)

        # --- 3. Khu vực chi tiết HÀNG 1 ---
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(20)

        # Group 1: Thiết bị
        gb_device_status = self.create_group_box("Tình trạng thiết bị")
        gb_layout_1 = QVBoxLayout()
        self.lbl_status_good = self.create_info_label("✅ Tốt: 0")
        self.lbl_status_broken = self.create_info_label("❌ Hỏng: 0")
        self.lbl_status_liquidation = self.create_info_label("⚠️ Đã thanh lý: 0")
        
        for lbl in [self.lbl_status_good, self.lbl_status_broken, self.lbl_status_liquidation]:
            gb_layout_1.addWidget(lbl)
        gb_layout_1.addStretch()
        gb_device_status.setLayout(gb_layout_1)
        row1_layout.addWidget(gb_device_status)

        # Group 2: Bảo trì
        gb_maint_status = self.create_group_box("Tình hình bảo trì")
        gb_layout_2 = QVBoxLayout()
        self.lbl_ticket_open = self.create_info_label("🔓 Phiếu mới báo cáo: 0")
        self.lbl_ticket_progress = self.create_info_label("🔄 Đang xử lý: 0")
        self.lbl_ticket_closed = self.create_info_label("🔒 Đã đóng: 0")

        for lbl in [self.lbl_ticket_open, self.lbl_ticket_progress, self.lbl_ticket_closed]:
            gb_layout_2.addWidget(lbl)
        gb_layout_2.addStretch()
        gb_maint_status.setLayout(gb_layout_2)
        row1_layout.addWidget(gb_maint_status)

        main_layout.addLayout(row1_layout)

        # --- 4. Khu vực chi tiết HÀNG 2 ---
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(20)

        # Group 3: Nhân sự
        gb_hr_status = self.create_group_box("Nhân sự và Phòng ban")
        gb_layout_3 = QVBoxLayout()
        self.lbl_total_depts = self.create_info_label("🏢 Số lượng phòng ban: 0")
        self.lbl_avg_emp = self.create_info_label("📊 TB nhân viên/phòng: 0")
        self.lbl_hr_note = self.create_info_label("ℹ️ Tổng nhân sự: 0")

        for lbl in [self.lbl_total_depts, self.lbl_avg_emp, self.lbl_hr_note]:
            gb_layout_3.addWidget(lbl)
        gb_layout_3.addStretch()
        gb_hr_status.setLayout(gb_layout_3)
        row2_layout.addWidget(gb_hr_status)

        # Group 4: Bàn giao
        gb_assign_status = self.create_group_box("Hoạt động Bàn giao")
        gb_layout_4 = QVBoxLayout()
        self.lbl_assign_active = self.create_info_label("⏳ Đang cho mượn: 0")
        self.lbl_assign_returned = self.create_info_label("↩️ Đã trả lại: 0")
        self.lbl_assign_total = self.create_info_label("📝 Tổng số phiếu: 0")

        for lbl in [self.lbl_assign_active, self.lbl_assign_returned, self.lbl_assign_total]:
            gb_layout_4.addWidget(lbl)
        gb_layout_4.addStretch()
        gb_assign_status.setLayout(gb_layout_4)
        row2_layout.addWidget(gb_assign_status)

        main_layout.addLayout(row2_layout)
        main_layout.addStretch()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def create_group_box(self, title):
        gb = QGroupBox(title)
        gb.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        # CSS FIX: 
        # 1. Tăng margin-top lên 30px để tiêu đề không bị cắt
        # 2. padding-top 10px để nội dung bên trong không dính sát viền trên
        gb.setStyleSheet("""
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 8px;
                margin-top: 30px; 
                background-color: #f9f9f9;
                color: #333; 
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                color: #e0e0e0; /* Màu tiêu đề sáng để nổi trên nền tối bên ngoài */
                background-color: transparent;
            }
        """)
        # Lưu ý: Vì QGroupBox nằm trên nền tối, nhưng background-color bên trong là #f9f9f9 (sáng).
        # Tiêu đề nằm ở margin (phần trong suốt hoặc nền tối của app).
        # Để dễ nhìn, ta set color tiêu đề là sáng (#e0e0e0) hoặc phải set background cho title.
        return gb

    def create_info_label(self, text):
        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 11))
        # Text bên trong GroupBox (nền trắng) nên màu chữ phải tối (#333)
        lbl.setStyleSheet("border: none; padding: 2px; color: #333;")
        return lbl

    def load_data(self):
        try:
            # 1. Fetch data
            devices = self.inventory_mgr.get_all_devices()
            employees = self.hr_mgr.get_all_employees()
            departments = self.hr_mgr.get_all_departments()
            
            # Assignment handling
            if hasattr(self.assignment_mgr, 'get_all_assignments'):
                all_assignments = self.assignment_mgr.get_all_assignments()
            else:
                all_assignments = self.assignment_mgr.get_active_assignments()

            tickets = self.maintenance_mgr.get_all_tickets()

            # 2. Statistics Calculation
            total_dev = len(devices)
            
            # Fix status check safely
            count_good = 0
            count_broken = 0
            count_retired = 0
            for d in devices:
                # Kiểm tra kỹ kiểu dữ liệu trả về của get_status
                # Giả sử d.get_quality_status() trả về Enum
                q_status = d.get_quality_status()
                # So sánh với Enum hoặc value của Enum
                if q_status == DeviceQualityStatus.GOOD or str(q_status) == str(DeviceQualityStatus.GOOD):
                    count_good += 1
                elif q_status == DeviceQualityStatus.BROKEN or str(q_status) == str(DeviceQualityStatus.BROKEN):
                    count_broken += 1
                elif q_status == DeviceQualityStatus.RETIRED or str(q_status) == str(DeviceQualityStatus.RETIRED):
                    count_retired += 1

            # Fix maintenance count
            count_reported = sum(1 for t in tickets if t.get_status() == MaintenanceStatus.REPORTED)
            count_resolved = sum(1 for t in tickets if t.get_status() == MaintenanceStatus.RESOLVED)
            count_closed = sum(1 for t in tickets if t.get_status() == MaintenanceStatus.CLOSED)

            total_emp = len(employees)
            total_dept = len(departments)
            avg_emp = round(total_emp / total_dept, 1) if total_dept > 0 else 0

            # Assignment Logic
            count_assign_active = 0
            count_assign_returned = 0
            for a in all_assignments:
                # Check return date safely
                r_date = a.get_return_date() if hasattr(a, 'get_return_date') else getattr(a, 'actual_return_date', None)
                # Nếu actual_return_date (private _Assignment__actual_return_date) không None thì là đã trả
                # Tuy nhiên nên dùng getter chuẩn: a.get_actual_return_date()
                if hasattr(a, 'get_actual_return_date'):
                    r_date = a.get_actual_return_date()
                
                if r_date: 
                    count_assign_returned += 1
                else:
                    count_assign_active += 1
            
            total_assign = len(all_assignments)

            # 3. Update UI
            self.card_total_devices.update_value(total_dev)
            self.card_assigned.update_value(count_assign_active)
            self.card_maintenance.update_value(count_broken)
            self.card_employees.update_value(total_emp)

            self.lbl_status_good.setText(f"✅ Tốt: {count_good}")
            self.lbl_status_broken.setText(f"❌ Hỏng: {count_broken}")
            self.lbl_status_liquidation.setText(f"⚠️ Đã thanh lý: {count_retired}")

            self.lbl_ticket_open.setText(f"🔓 Phiếu mới báo cáo: {count_reported}")
            self.lbl_ticket_progress.setText(f"🔄 Đang xử lý: {count_resolved}")
            self.lbl_ticket_closed.setText(f"🔒 Đã đóng: {count_closed}")

            self.lbl_total_depts.setText(f"🏢 Số lượng phòng ban: {total_dept}")
            self.lbl_avg_emp.setText(f"📊 TB nhân viên/phòng: {avg_emp}")
            self.lbl_hr_note.setText(f"ℹ️ Tổng nhân sự: {total_emp}")

            self.lbl_assign_active.setText(f"⏳ Đang cho mượn: {count_assign_active}")
            self.lbl_assign_returned.setText(f"↩️ Đã trả lại: {count_assign_returned}")
            self.lbl_assign_total.setText(f"📝 Tổng số phiếu: {total_assign}")

        except Exception as e:
            print(f"Lỗi load dashboard: {e}")
            import traceback
            traceback.print_exc()