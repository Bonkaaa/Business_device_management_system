from entities import MaintenanceTicket
from utils.constant_class import MaintenanceStatus
from entities import Device, Employee
from utils.id_generators import generate_ticket_id as generate_maintenance_ticket_id
from utils.constant_class import DeviceStatus, DeviceQualityStatus, AssignmentStatus
from datetime import datetime
from database import DatabaseManager
from .inventory import Inventory
from .hr_manager import HRManager

class MaintenanceManager:
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)

    def set_managers(self, inventory_manager: Inventory, hr_manager: HRManager) -> None:
        self.inventory_manager = inventory_manager
        self.hr_manager = hr_manager

    def create_ticket(
        self,
        issue_description: str,
        device: Device,
        reporter: Employee
    ) -> MaintenanceTicket:
        ticket_id = generate_maintenance_ticket_id()
        reported_date = datetime.now()

        # Query to insert new maintenance ticket
        query_ticket = """
            INSERT INTO maintenance_tickets (ticket_id, device_id, reporter_id, issue_description, status, reported_date, technician_notes, date_resolved, cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        query_device = """
            UPDATE devices
            SET status = ?, quality_status = ?
            WHERE device_id = ?
        """

        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            device_id = device.get_id()
            reporter_id = reporter.get_id()

            technician_notes = f"[Khởi tạo] Vào ngày {reported_date.isoformat()}, phiếu bảo trì {ticket_id} đã được tạo cho thiết bị {device_id} bởi nhân viên {reporter_id} với mô tả sự cố: {issue_description}.\n"

            # Insert maintenance ticket
            cursor.execute(query_ticket, (
                ticket_id,
                device_id,
                reporter_id,
                issue_description,
                MaintenanceStatus.REPORTED.value,
                reported_date,
                technician_notes,
                None,
                None
            ))

            # Update device status and quality status
            cursor.execute(query_device, (
                DeviceStatus.MAINTENANCE.value,
                DeviceQualityStatus.BROKEN.value,
                device_id
            ))

            conn.commit()
            conn.close()

            return MaintenanceTicket(
                ticket_id=ticket_id,
                issue_description=issue_description,
                status=MaintenanceStatus.REPORTED,
                reported_date=reported_date,
                technician_notes=technician_notes,
                date_resolved=None,
                costs=None,
                device=device,
                reporter=reporter
            )
        
        except Exception as e:
            print(f"Lỗi khi tạo phiếu bảo trì: {e}")
            return None
        
    def resolve_ticket(
        self,
        ticket_id: str,
        technician_notes: str | None = None,
        costs: float | None = None
    ):
        date_resolved = datetime.now()

        current_ticket = self.search_ticket_by_id(ticket_id)

        if not current_ticket:
            print(f"Phiếu bảo trì với ID {ticket_id} không tồn tại.")
            return
        
        updated_notes = current_ticket.to_dict().get("technician_notes", "")
        updated_notes += f"[Giải quyết] Vào ngày {date_resolved.isoformat()}, phiếu bảo trì {ticket_id} đã được giải quyết. Tiền công: {costs if costs is not None else 'N/A'}.\n"
        if technician_notes:
            updated_notes += f" Ghi chú kỹ thuật viên: {technician_notes}\n"

        query = """
            UPDATE maintenance_tickets
            SET status = ?, date_resolved = ?, technician_notes = ?, cost = ?
            WHERE ticket_id = ?
        """

        try:
            params = (
                MaintenanceStatus.RESOLVED.value,
                date_resolved.isoformat(),
                updated_notes,
                costs,
                ticket_id
            )
            self.db_manager.execute_query(query, params)

        except Exception as e:
            print(f"Lỗi khi giải quyết phiếu bảo trì: {e}")


    def close_ticket(
        self,
        ticket_id: str,
        is_repaired: bool,
    ):
        
        ticket = self.search_ticket_by_id(ticket_id)

        if not ticket:
            print(f"Phiếu bảo trì với ID {ticket_id} không tồn tại.")
            return
        
        device = ticket.get_device()

        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            if is_repaired:
                # Check if device was assigned
                cursor.execute("""
                    SELECT assigned_to FROM devices WHERE device_id = ?
                """, (device.get_id(),))
                row = cursor.fetchone()

                if row and row[0]:
                    new_status = DeviceStatus.ASSIGNED.value
                else:
                    new_status = DeviceStatus.AVAILABLE.value

                cursor.execute("""
                    UPDATE devices
                    SET status = ?, quality_status = ?
                    WHERE device_id = ?
                """, (
                    new_status,
                    DeviceQualityStatus.GOOD.value,
                    device.get_id()
                ))

            else:
                # Update device
                cursor.execute("""
                    UPDATE devices
                    SET status = ?, quality_status = ?, assigned_to = NULL
                    WHERE device_id = ?
                """, (
                    DeviceStatus.OUT_OF_SERVICE.value,
                    DeviceQualityStatus.RETIRED.value,
                    device.get_id()
                ))

                # Update assignment if exists
                assignemnt = self.assignment_manager.get_active_assignment_by_device_id(device.get_id())
                if assignemnt:
                    assignment_id = assignemnt.get_id()
                    cursor.execute("""
                        UPDATE assignments
                        SET status = ?, actual_return_date = ?, quality_status = ?, notes = ?
                        WHERE assignment_id = ?
                    """, (
                        AssignmentStatus.CLOSED.value,
                        datetime.now().isoformat(),
                        DeviceQualityStatus.BROKEN.value,
                        f"[Đóng] Do thiết bị {device.get_id()} bị hỏng và không thể sửa chữa nên đã được ngừng sử dụng.",      
                        assignment_id
                    ))
            
            # Update maintenance ticket status
            cursor.execute("""
                UPDATE maintenance_tickets
                SET status = ?
                WHERE ticket_id = ?
            """, (
                MaintenanceStatus.CLOSED.value,
                ticket_id
            ))

            conn.commit()
            conn.close()
            print(f"Đóng phiếu bảo trì {ticket_id} thành công.")
        except Exception as e:
            print(f"Lỗi khi đóng phiếu bảo trì: {e}")

    def search_ticket_by_id(self, ticket_id: str) -> MaintenanceTicket | None:
        query = "SELECT * FROM maintenance_tickets WHERE ticket_id = ?"
        params = (ticket_id,)
        row = self.db_manager.fetch_one(query, params)
        if row:
            return self._row_to_ticket(row)
        return None
    
    def get_all_tickets(self) -> list[MaintenanceTicket]:
        query = "SELECT * FROM maintenance_tickets"
        rows = self.db_manager.fetch_all(query)
        tickets = []
        for row in rows:
            ticket = self._row_to_ticket(row)
            tickets.append(ticket)
        return tickets
    
    def get_tickets_by_reporter_id(self, reporter_id: str) -> list[MaintenanceTicket]:
        query = "SELECT * FROM maintenance_tickets WHERE reporter_id = ?"
        params = (reporter_id,)
        rows = self.db_manager.fetch_all(query, params)
        tickets = []
        for row in rows:
            ticket = self._row_to_ticket(row)
            tickets.append(ticket)
        return tickets

    def _row_to_ticket(self, row) -> MaintenanceTicket:
        device = self.inventory_manager.get_device_by_id(row['device_id'])
        reporter = self.hr_manager.get_employee_by_id(row['reporter_id'])

        reported_date = datetime.fromisoformat(row['reported_date'])
        date_resolved = datetime.fromisoformat(row['date_resolved']) if row['date_resolved'] else None

        return MaintenanceTicket(
            ticket_id=row['ticket_id'],
            issue_description=row['issue_description'],
            status=MaintenanceStatus(row['status']),
            reported_date=reported_date,
            date_resolved=date_resolved,
            technician_notes=row['technician_notes'],
            costs=row['cost'],
            device=device,
            reporter=reporter
        )





        
        
        



    

    
    

    