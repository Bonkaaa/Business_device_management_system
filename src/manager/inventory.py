from utils.utils import save_to_json, load_from_json
import json
from database import DatabaseManager
from entities import Device
from datetime import datetime
from typing import Dict, Any
from utils.id_generators import generate_device_id
from utils.constant_class import DeviceStatus, DeviceQualityStatus

class Inventory:
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)
        self.hr_manager = None
        self.assignment_manager = None

    def set_managers(self, hr_manager, assignment_manager) -> None:
        self.hr_manager = hr_manager
        self.assignment_manager = assignment_manager

    def add_device(
        self,
        category: str,
        name: str,
        specifications: Dict[str, Any],
        purchase_date: datetime | None = None,
    ):
        device_id = generate_device_id()
        spec_json = json.dumps(specifications)

        query = """
        INSERT INTO devices (device_id, name, category, status, quality_status, purchase_date, specifications)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            device_id,
            name,
            category,
            DeviceStatus.AVAILABLE.value,
            DeviceQualityStatus.GOOD.value,
            purchase_date,
            spec_json,
        )
        self.db_manager.execute_query(query, params)
    
    def remove_device(self, device_id: str) -> None:
        query = "DELETE FROM devices WHERE device_id = ?"
        params = (device_id,)
        self.db_manager.execute_query(query, params)

    def get_all_available_devices(self) -> list[Device]:
        query = "SELECT * FROM devices WHERE status = ?"
        params = (DeviceStatus.AVAILABLE.value,)
        rows = self.db_manager.fetch_all(query, params)

        devices = []
        for row in rows:
            specifications = json.loads(row['specifications'])
            device = Device(
                device_id=row['device_id'],
                name=row['name'],
                category=row['category'],
                status=DeviceStatus(row['status']),
                purchase_date=row['purchase_date'],
                specifications=specifications,
                assignment_manager=self.assignment_manager,
            )
            devices.append(device)
        return devices
    
    def get_device_by_id(self, device_id: str) -> Device | None:
        query = "SELECT * FROM devices WHERE device_id = ?"
        params = (device_id,)
        row = self.db_manager.fetch_one(query, params)

        if row:
            specifications = json.loads(row['specifications'])
            return Device(
                device_id=row['device_id'],
                name=row['name'],
                category=row['category'],
                status=DeviceStatus(row['status']),
                purchase_date=row['purchase_date'],
                specifications=specifications,
                assignment_manager=self.assignment_manager,
            )
        return None
    
    def search_device_by_category(self, category: str) -> list[Device]:
        query = "SELECT * FROM devices WHERE category = ?"
        params = (category,)
        rows = self.db_manager.fetch_all(query, params)

        devices = []
        for row in rows:
            spec = json.loads(row['specifications'])
            device = Device(
                device_id=row['device_id'],
                name=row['name'],
                category=row['category'],
                status=DeviceStatus(row['status']),
                purchase_date=row['purchase_date'],
                specifications=spec,
                assignment_manager=self.assignment_manager,
            )
            devices.append(device)

        return devices
    
    def filter_devices_by_device_status(self, status: DeviceStatus) -> list[Device]:
        query = "SELECT * FROM devices WHERE status =?"
        params = (status,)
        rows = self.db_manager.fetch_all(query, params)

        devices = []
        for row in rows:
            spec = json.loads(row['specifications'])
            device = Device(
                device_id=row['device_id'],
                name=row['name'],
                category=row['category'],
                status=DeviceStatus(row['status']),
                purchase_date=row['purchase_date'],
                specifications=spec,
                assignment_manager=self.assignment_manager,
            )
            devices.append(device)

        return devices
    
    def check_device_quality_status(self, device_id: str) -> bool:
        query = "SELECT quality_status FROM devices WHERE device_id = ?"
        params = (device_id,)
        row = self.db_manager.fetch_one(query, params)

        if row:
            quality_status = DeviceQualityStatus(row['quality_status'])
            if quality_status == DeviceQualityStatus.GOOD:
                return True
            return False
        else:
            raise ValueError(f"Thiết bị với ID {device_id} không tồn tại trong kho.")

    def get_all_devices(self):
        query = "SELECT * FROM devices"
        rows = self.db_manager.fetch_all(query)

        devices = []
        for row in rows:
            spec = json.loads(row['specifications'])

            device = Device(
                device_id=row['device_id'],
                name=row['name'],
                category=row['category'],
                status=DeviceStatus(row['status']),
                purchase_date=row['purchase_date'],
                specifications=spec,
                assignment_manager=self.assignment_manager,
            )
            if row['quality_status']:
                device.update_quality_status(DeviceQualityStatus(row['quality_status']))
            devices.append(device)

        return devices
    
    def update_device_status(
        self,
        device_id: str,
        new_status: DeviceStatus,
    ) -> None:
        query = """
            UPDATE devices
            SET status = ?
            WHERE device_id = ?
        """
        params = (new_status.value, device_id)
        self.db_manager.execute_query(query, params)

    def update_device_and_quality_status(
        self,
        device_id: str,
        new_status: DeviceStatus,
        new_quality_status: DeviceQualityStatus,
    ) -> None:
        query = """
        UPDATE devices
        SET status = ?, quality_status = ?
        WHERE device_id = ?
        """
        params = (new_status.value, new_quality_status.value, device_id)
        self.db_manager.execute_query(query, params)

    def get_devices_by_assignee_id(self, assignee_id: str) -> list[Device]:
        # Get assignments from AssignmentManager
        assignments = self.assignment_manager.get_all_assignments_by_assignee_id(assignee_id)

        devices = []

        for assignment in assignments:
            device = self.get_device_by_id(assignment.get_device().get_id())
            if device:
                devices.append(device)
        return devices
        

        
        