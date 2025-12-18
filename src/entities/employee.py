from base.assignee import Assignee
from device import Device
from typing import Bool
from .department import Department

class Employee(Assignee):
    def __init__(
        self,
        name: str,
        employee_id: str,
        email: str,
        phone_number: str,
        position: str,
        department: Department
    ):
        super().__init__(name, employee_id)

        # Public attributes
        self.email = email
        self.phone_number = phone_number
        
        # Protected attributes
        self._position = position
        self._department = department


    def assign_device(self, device: Device) -> Bool:
        device_id = device.get_id()
        if device_id not in self.__assigned_devices:
            self.__assigned_devices.append(device_id)
            return True
        return False


    def unassign_device(self, device: Device) -> Bool:
        device_id = device.get_id()
        if device_id in self.__assigned_devices:
            self.__assigned_devices.remove(device_id)
            return True
        return False
    
    def get_contact_info(self) -> str:
        return f"Email: {self.email}, Phone: {self.phone_number}"
    
    def get_assignee_type(self) -> str:
        return "Employee"
    
    def get_department(self) -> Department:
        return self._department
    
    def to_dict(self) -> dict:
        return {
            "employee_id": self.get_id(),
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "position": self._position,
            "assigned_devices": self.__assigned_devices,
        }
    
    def report_issue_for_personal_device(self, device: Device, issue_description: str) -> str:
        return f"Báo cáo sự cố cho thiết bị cá nhân {device.name} ({device.get_id()}) của nhân viên {self.name} : {issue_description}"
    
    def report_issue_for_department_device(self, device: Device, issue_description: str) -> str:
        department = self._department
        return f"Báo cáo sự cố cho thiết bị của phòng ban {department.get_name()} - thiết bị {device.name} ({device.get_id()}) bởi nhân viên {self.name} : {issue_description}"