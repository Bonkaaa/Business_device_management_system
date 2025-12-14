from base.assignee import Assignee
from device import Device
from typing import Bool

class Employee(Assignee):
    def __init__(
        self,
        name: str,
        employee_id: str,
        email: str,
        phone_number: str,
        position: str,
    ):
        super().__init__(name, employee_id)

        # Public attributes
        self.email = email
        self.phone_number = phone_number
        
        # Protected attributes
        self._position = position


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
    
    def get_contact_info(self) -> str:
        return f"Email: {self.email}, Phone: {self.phone_number}"
    
    def get_assignee_type(self) -> str:
        return "Employee"
    
    def to_dict(self) -> dict:
        return {
            "employee_id": self.get_id(),
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "position": self._position,
            "assigned_devices": self._assigned_devices,
        }
    
