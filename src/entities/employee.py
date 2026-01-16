from base import Assignee
from utils.constant_class import DeviceQualityStatus, DeviceStatus
from .device import Device
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .department import Department

class Employee(Assignee):
    def __init__(
        self,
        name: str,
        employee_id: str,
        email: str,
        phone_number: str,
        position: str,
        department: Optional["Department"] = None,
        inventory_manager = None,
    ):
        super().__init__(name, employee_id)

        # Public attributes
        self.email = email
        self.phone_number = phone_number
        
        # Protected attributes
        self._position = position
        self._department = department
        self._inventory_manager = inventory_manager
    
    def get_assignee_type(self) -> str:
        return "Employee"
    
    def get_department(self) -> "Department":
        return self._department
    
    def get_position(self) -> str:
        return self._position
    
    def to_dict(self) -> dict:
        return {
            "employee_id": self.get_id(),
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "position": self._position,
        }
    
    def get_assigned_devices(self) -> list[Device]:
        if self._inventory_manager:
            return self._inventory_manager.get_devices_by_assignee_id(self.get_id())
        return []
    
    def assign_device(self, device) -> None:
        if self._inventory_manager:
            self._inventory_manager.update_device_status(
                device.get_id(), 
                DeviceStatus.ASSIGNED, 
            )
    
    def unassign_device(
        self, 
        device, 
        return_quality_status: DeviceQualityStatus,
        device_status: DeviceStatus
    ) -> None:
        if self._inventory_manager:
            self._inventory_manager.update_device_and_quality_status(
                device.get_id(), 
                device_status, 
                return_quality_status,
            )
    
    # def report_issue_for_personal_device(self, device: Device, issue_description: str) -> str:
    #     return f"Báo cáo sự cố cho thiết bị cá nhân {device.name} ({device.get_id()}) của nhân viên {self.name} : {issue_description}"
    
    # def report_issue_for_department_device(self, device: Device, issue_description: str) -> str:
    #     department = self._department
    #     return f"Báo cáo sự cố cho thiết bị của phòng ban {department.get_name()} - thiết bị {device.name} ({device.get_id()}) bởi nhân viên {self.name} : {issue_description}"