from entities import Assignment, Device
from base import Assignee
from datetime import datetime
from utils.id_generators import generate_assignment_id
from utils.constant_class import DeviceQualityStatus, DeviceStatus, AssignmentStatus
from database import DatabaseManager
from .hr_manager import HRManager
from .inventory import Inventory


class AssignmentManager:
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)

    def set_managers(self, inventory_manager: Inventory, hr_manager: HRManager) -> None:
        self.inventory_manager = inventory_manager
        self.hr_manager = hr_manager

    def create_assignment(
        self,
        device: Device,
        assignee: Assignee,
        expected_return_date: datetime | None,
        quality_status: DeviceQualityStatus | None
    ):
        if self.has_active_assignment(device.get_id()):
            raise Exception(f"Thiết bị {device.get_id()} đang có phiếu bàn giao ở trạng thái mở. Không thể tạo phiếu mới.")
        
        assignment_id = generate_assignment_id()
        initial_date = datetime.now()
        initial_date_str = initial_date.isoformat()

        if quality_status is not None:
            quality_status_value = quality_status.value
        else:
            quality_status_value = ""

        device_id = device.get_id()
        assignee_id = assignee.get_id()
        expected_return_date_str = expected_return_date.isoformat() if expected_return_date else None

        current_assignee_devices = assignee.get_assigned_devices()
        current_assignee_devices.append(f"{device.get_id()}-{device.name}")
        current_assignee_devices_str = ",".join(current_assignee_devices)

        # Check if assignee is employee or department to handle assigned_devices properly
        if assignee_id.startswith("EMP"):
            flag_employee = True
        else:
            flag_employee = False


        query_insert = """
            INSERT INTO assignments (
                assignment_id, initial_date, expected_return_date, actual_return_date, status, quality_status, notes, device_id, device_name, assignee_id, assignee_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        query_update_device = """
            UPDATE devices
            SET status = ?, assigned_to = ?
            WHERE device_id = ?
        """

        table_name = "employees" if flag_employee else "departments"
        id = "employee_id" if flag_employee else "department_id"
        query_update_assignee = f"""
            UPDATE {table_name}
            SET assigned_devices =  ?
            WHERE {id} = ?
        """

        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            # Insert new assignment
            cursor.execute(query_insert, (
                assignment_id,
                initial_date_str,
                expected_return_date_str,
                "",
                AssignmentStatus.OPEN.value,
                quality_status_value,
                "",
                device_id,
                device.name,
                assignee_id,
                assignee.name,
            ))

            # Update device status and assigned_to
            cursor.execute(query_update_device, (
                DeviceStatus.ASSIGNED.value,
                assignee_id,
                device_id
            ))

            # Update assignee's assigned devices
            cursor.execute(query_update_assignee, (
                current_assignee_devices_str,
                assignee_id
            ))

            conn.commit()
            conn.close()

            
            device.update_device_status(DeviceStatus.ASSIGNED)
            device.update_assigned_to(assignee.name)

            return Assignment(
                assignment_id=assignment_id,
                initial_date=initial_date,
                expected_return_date=expected_return_date,
                actual_return_date=None,
                status=None,
                notes="",
                device=device,
                assignee=assignee
            )
        except Exception as e:
            print(f"Error creating assignment: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None
        
    def close_assignment(
        self,
        assignment_id: str,
        return_quality_status: DeviceQualityStatus,
        actual_return_date: str | None = None,
        broken_status: bool = False,
    ):
        actual_return_date_str = actual_return_date

        new_device_status = DeviceStatus.OUT_OF_SERVICE if broken_status else DeviceStatus.AVAILABLE

        query_update_assignment = """
            UPDATE assignments
            SET quality_status = ?, actual_return_date = ?, status = ?, notes = notes || ?
            WHERE assignment_id = ?
        """

        query_update_device = """
            UPDATE devices
            SET status = ?, assigned_to = ?, quality_status = ?
            WHERE device_id = (
                SELECT device_id FROM assignments WHERE assignment_id = ?
            )
        """

        note_append = f"[Đóng] Trả vào ngày {actual_return_date}, tình trạng: {return_quality_status.value}.\n"

        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            # Update assignment
            cursor.execute(query_update_assignment, (
                return_quality_status.value,
                actual_return_date_str,
                AssignmentStatus.CLOSED.value,
                note_append,
                assignment_id
            ))

            # Update device
            cursor.execute(query_update_device, (
                new_device_status.value,
                None,
                return_quality_status.value,
                assignment_id
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Lỗi khi đóng assignment: {e}")
        
    # ==== Getters and Searchers ====
    def get_assignment_by_id(self, assignment_id: str) -> Assignment | None:
        query = "SELECT * FROM assignments WHERE assignment_id = ?"
        params = (assignment_id,)
        row = self.db_manager.fetch_one(query, params)

        if not row:
            return None
        return self._row_to_assignment(row)
    
    def get_active_assignment_by_assignee_id(self, assignee_id: str) -> list[Assignment] | None:
        query = "SELECT * FROM assignments WHERE assignee_id = ? AND status = ?"
        params = (assignee_id, AssignmentStatus.OPEN.value)
        rows = self.db_manager.fetch_all(query, params)

        if not rows:
            return None
        
        assignments = []
        for row in rows:
            assignment = self._row_to_assignment(row)
            assignments.append(assignment)
        return assignments
    
    def get_active_assignment_by_device_id(self, device_id: str) -> Assignment | None:
        query = "SELECT * FROM assignments WHERE device_id = ? AND status = ?"
        params = (device_id, AssignmentStatus.OPEN.value)
        row = self.db_manager.fetch_one(query, params)

        if not row:
            return None
        return self._row_to_assignment(row)
        
    
    def get_active_assignments(self) -> list[Assignment]:
        query = "SELECT * FROM assignments WHERE status = ?"
        params = (AssignmentStatus.OPEN.value,)
        rows = self.db_manager.fetch_all(query, params)

        assignments = []
        for row in rows:
            assignment = self._row_to_assignment(row)
            assignments.append(assignment)
        return assignments
    
    def get_overdue_assignments(self) -> list[Assignment]:
        current_date = datetime.now()
        query = "SELECT * FROM assignments WHERE status = ? AND expected_return_date < ?"
        params = (AssignmentStatus.OPEN.value, current_date)
        rows = self.db_manager.fetch_all(query, params)

        assignments = []
        for row in rows:
            assignment = self._row_to_assignment(row)
            assignments.append(assignment)
        return assignments
    
    def get_all_assignments(self) -> list[Assignment]:
        query = "SELECT * FROM assignments"
        rows = self.db_manager.fetch_all(query)

        assignments = []
        for row in rows:
            assignment = self._row_to_assignment(row)
            assignments.append(assignment)
        return assignments
    
    def has_active_assignment(self, device_id: str) -> bool:
        query = "SELECT COUNT(*) as count FROM assignments WHERE device_id = ? AND status = ?"
        params = (device_id, AssignmentStatus.OPEN.value)
        row = self.db_manager.fetch_one(query, params)

        if row and row['count'] > 0:
            return True
        return False
        
    # ======= Helper Methods =======
    def _row_to_assignment(self, row) -> Assignment:
        device = self.inventory_manager.get_device_by_id(row['device_id'])
        
        assignee = self.hr_manager.get_assignee_by_id(row['assignee_id'])
        
        init_date = datetime.fromisoformat(row['initial_date'])
        expected_return_date = datetime.fromisoformat(row['expected_return_date']) if row['expected_return_date'] else None
        actual_return_date = datetime.fromisoformat(row['actual_return_date']) if row['actual_return_date'] else None

        status = AssignmentStatus(row['status'])

        return Assignment(
            assignment_id=row['assignment_id'],
            initial_date=init_date,
            expected_return_date=expected_return_date,
            actual_return_date=actual_return_date,
            status=status,
            notes=row['notes'],
            device=device,
            assignee=assignee
        )
        
            

           





    

        
        

        

