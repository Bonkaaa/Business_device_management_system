class Department: 
    def __init__(
        self,
        department_id: str,
        name: str,
        manager_id: str | None,
        location: str
    ):
        self.department_id = department_id
        self.name = name
        self.manager_id = manager_id
        self.location = location

        self.employee_ids = []
        
        self.device_ids = []

    def add_employee(self, employee_id: str):
        if employee_id not in self.employee_ids:
            self.employee_ids.append(employee_id)
            return True
        return False
    
    def remove_employee(self, employee_id: str):
        if employee_id in self.employee_ids:
            self.employee_ids.remove(employee_id)
            if employee_id == self.manager_id:
                self.manager_id = None
            return True
        return False
    
    def assign_shared_device(self, device_id: str):
        if device_id not in self.device_ids:
            self.device_ids.append(device_id)
            return True
        return False
    
    def remove_shared_device(self, device_id: str):
        if device_id in self.device_ids:
            self.device_ids.remove(device_id)
            return True
        return False
    
    def __str__(self):
        manager_str = f"(Manager: {self.manager_id})" if self.manager_id else ""
        return f"[{self.dept_id}] {self.name} - {self.location} | {len(self.employee_ids)} NV | {len(self.device_ids)} TB {manager_str}"
    
    def to_dict(self):
        return {
            "Department ID": self.department_id,
            "Name": self.name,
            "Manager ID": self.manager_id,
            "Location": self.location,
            "Employee IDs": self.employee_ids,
            "Device IDs": self.device_ids
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        dept = cls(
            department_id=data.get("Department ID"),
            name=data.get("Name"),
            manager_id=data.get("Manager ID"),
            location=data.get("Location")
        )
        dept.employee_ids = data.get("Employee IDs", [])
        dept.device_ids = data.get("Device IDs", [])
        return dept