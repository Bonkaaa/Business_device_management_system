from entities import Assignment, Device
from base import Assignee
from datetime import datetime
from utils.id_generators import generate_assignment_id
from utils.constant_class import DeviceQualityStatus, DeviceStatus, AssignmentStatus
from database import DatabaseManager
from .hr_manager import HRManager
from .inventory import Inventory


class AssignmentManager:
    def __init__(self, inventory_manager: Inventory, hr_manager: HRManager, db_path: str):
        self.db_manager = DatabaseManager(db_path)
        self.inventory_manager = inventory_manager
        self.hr_manager = hr_manager

    def create_assignment(
        self,
        device: Device,
        assignee: Assignee,
        expected_return_date: str | None,
        quality_status: DeviceQualityStatus | None
    ):
        assignment_id = generate_assignment_id()
        initial_date = datetime.now()

        if quality_status is not None:
            quality_status_value = quality_status.value

        device_id = device.get_id()
        assignee_id = assignee.get_id()

        query_insert = """
            INSERT INTO assignments (
                assignment_id, initial_date, expected_return_date, quality_status, notes, device_id, assignee_id, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        query_update_device = """
            UPDATE devices
            SET status = ?, assigned_to = ?
            WHERE device_id = ?
        """

        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()

            # Insert new assignment
            cursor.execute(query_insert, (
                assignment_id,
                initial_date,
                expected_return_date,
                quality_status_value if quality_status is not None else None,
                "",
                device_id,
                assignee_id,
                AssignmentStatus.OPEN.value
            ))

            # Update device status and assigned_to
            cursor.execute(query_update_device, (
                DeviceStatus.ASSIGNED.value,
                assignee_id,
                device_id
            ))

            # MISSING UPDATE ASSIGNEE'S ASSIGNED DEVICES IF NEEDED

            conn.commit()
            conn.close()

            return Assignment(
                assignment_id=assignment_id,
                initial_date=initial_date,
                expected_return_date=expected_return_date,
                quality_status=quality_status,
                notes="",
                device=device,
                assignee=assignee
            )
        except Exception as e:
            print(f"Error creating assignment: {e}")
            return None
        
    def close_assignment(
        self,
        assignment_id: str,
        return_quality_status: DeviceQualityStatus,
        actual_return_date: datetime | None = None,
        return_date_today: bool = True,
        broken_status: bool = False,
    ):
        if return_date_today:
            actual_return_date = datetime.now()

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
                actual_return_date,
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
        
    # ======= Helper Methods =======
    def _row_to_assignment(self, row) -> Assignment:
        device = self.inventory_manager.get_device_by_id(row['device_id'])
        
        assignee = self.hr_manager.get_assignee_by_id(row['assignee_id'])
        
        init_date = datetime.fromisoformat(row['initial_date'])
        expected_return_date = datetime.fromisoformat(row['expected_return_date']) if row['expected_return_date'] else None

        return Assignment(
            assignment_id=row['assignment_id'],
            initial_date=init_date,
            expected_return_date=expected_return_date,
            quality_status=DeviceQualityStatus(row['quality_status']) if row['quality_status'] else None,
            notes=row['notes'],
            device=device,
            assignee=assignee
        )
        
        
            

           





    

        
        

        

