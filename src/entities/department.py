from base import Assignee
from .employee import Employee
from .device import Device

class Department(Assignee):
    def __init__(
        self, 
        name: str, 
        department_id: str,
        manager: Employee | None,
        location: str,
        assigned_devices: list | None = None,
        employees: list | None = None
    ):
        super().__init__(name, department_id, assigned_devices)

        # Protected attributes
        self._location = location
        self._manager = manager

        # Private attributes
        self.__employees = employees if employees is not None else []

    def get_employees(self) -> list:
        return self.__employees
    
    def add_employee(self, employee: Employee) -> bool:
        """Add employee to the department"""
        if employee not in self.__employees:
            self.__employees.append(employee)
            return True
        return False
    
    def remove_employee(self, employee: Employee) -> bool:
        """Remove employee from the department"""
        if employee in self.__employees:
            self.__employees.remove(employee)
            return True
        return False
    
    def get_name(self) -> str:
        return self.name
    
    def get_location(self) -> str:
        return self._location
    
    def get_manager(self) -> Employee | None:
        return self._manager

    def assign_device(self, device: Device) -> bool:
        device_id = device.get_id()
        if device_id not in self.__assigned_devices:
            self.__assigned_devices.append(device_id)
            return True
        return False
    
    def unassign_device(self, device: Device) -> bool:
        device_id = device.get_id()
        if device_id in self.__assigned_devices:
            self.__assigned_devices.remove(device_id)
            return True
        return False
    
    def get_contact_info(self):
        return f"Department Location: {self._location}, Manager: {self._manager.get_name()}"

    def get_assignee_type(self) -> str:
        return "Department"
    
    def to_dict(self) -> dict:
        return {
            "department_id": self.get_id(),
            "name": self.name,
            "location": self._location,
            "manager": self._manager.to_dict(),
            "assigned_devices": self.__assigned_devices,
            "employees": [emp.get_name() for emp in self.__employees],
        }
    
    

    

    

        
    