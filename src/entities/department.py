from base import Assignee
from utils.constant_class import DeviceQualityStatus, DeviceStatus
from .employee import Employee
from .device import Device

class Department(Assignee):
    def __init__(
        self, 
        name: str, 
        department_id: str,
        manager: Employee | None,
        location: str,
        hr_manager = None,
        inventory_manager = None,
    ):
        super().__init__(name, department_id)

        # Protected attributes
        self._location = location
        self._manager = manager
        self._hr_manager = hr_manager
        self._inventory_manager = inventory_manager

    def get_name(self) -> str:
        return self.name
    
    def get_location(self) -> str:
        return self._location
    
    def get_manager(self) -> Employee | None:
        return self._manager
    
    def get_assignee_type(self) -> str:
        return "Department"
    
    def to_dict(self) -> dict:
        return {
            "department_id": self.get_id(),
            "name": self.name,
            "location": self._location,
            "manager": self._manager.to_dict(),
        }
    
    def get_employees(self):
        if self._hr_manager:
            return self._hr_manager.get_employees_by_department_id(self.get_id())
        return []
    
    def get_assigned_devices(self) -> list[Device]:
        if self._inventory_manager:
            return self._inventory_manager.get_devices_by_assignee_id(self.get_id())
        return []
    
    def assign_device(self, device: "Device") -> None:
        if self._inventory_manager:
            self._inventory_manager.update_device_status(
                device.get_id(), 
                DeviceStatus.ASSIGNED, 
            )

    def unassign_device(
        self, 
        device: "Device", 
        return_quality_status: DeviceQualityStatus,
        device_status: DeviceStatus,
    ) -> None:
        if self._inventory_manager:
            self._inventory_manager.update_device_and_quality_status(
                device.get_id(), 
                device_status, 
                return_quality_status,
            )
    
    

    

    

        
    