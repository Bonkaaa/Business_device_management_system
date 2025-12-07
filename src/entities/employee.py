from typing import Bool

class Employee:
    def __init__(
        self,
        id,
        name, 
        department,
        email,
        phone_number
    ):
        self.employee_id = id
        self.name = name
        self.department = department
        self.email = email
        self.phone_number = phone_number
        self.assigned_devices = []  # List to hold assigned devices

    def assign_device(
        self,
        device_id
    ) -> Bool:
        if device_id not in self.assigned_devices:
            self.assigned_devices.append(device_id)
            return True
        return False
    
    def remove_device(
        self,
        device_id
    ):
        if device_id in self.assigned_devices:
            self.assigned_devices.remove(device_id)
            return True
        return False
    
    def __str__(self):
        return f"[{self.employee_id}] {self.name} - {self.department} (Đang giữ {len(self.assigned_devices)} thiết bị)"
    
    def to_dict(self):
        return {
            "Employee ID": self.employee_id,
            "Name": self.name,
            "Department": self.department,
            "Email": self.email,
            "Phone Number": self.phone_number,
            "Assigned Devices": self.assigned_devices
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        emp = cls(
            id=data.get("Employee ID"),
            name=data.get("Name"),
            department=data.get("Department"),
            email=data.get("Email"),
            phone_number=data.get("Phone Number")
        )
        emp.assigned_devices = data.get("Assigned Devices", [])
        return emp