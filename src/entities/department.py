from base.assignee import Assignee
from employee import Employee
from device import Device
from typing import Bool

class Department(Assignee):
    def __init__(
        self, 
        name: str, 
        department_id: str,
        manager: Employee,
        location: str
    ):
        super().__init__(name, department_id)

        # Public attributes
        self.location = location

        # Protected attributes
        self._manager = manager

        self.__employees = []

    def get_employees(self) -> list:
        return self.__employees

    def assign_device(self, device: Device) -> Bool:
        device_id = device.get_id()
        if device_id not in self._assigned_devices:
            self._assigned_devices.append(device_id)
            return True
        return False
    
    def unassign_device(self, device: Device) -> Bool:
        device_id = device.get_id()
        if device_id in self._assigned_devices:
            self._assigned_devices.remove(device_id)
            return True
        return False
    
    def get_contact_info(self):
        return f"Department Location: {self.location}, Manager: {self._manager.get_name()}"

    def get_assignee_type(self) -> str:
        return "Department"
    
    def to_dict(self) -> dict:
        return {
            "department_id": self.get_id(),
            "name": self.name,
            "location": self.location,
            "manager": self._manager.to_dict(),
            "assigned_devices": self._assigned_devices,
            "employees": [emp.get_name() for emp in self.__employees],
        }
    
    

    

    

        
    