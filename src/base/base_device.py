from abc import ABC, abstractmethod
from datetime import datetime

class BaseDevice(ABC):
    def __init__(self, device_id: str, device_name: str, price: float, purcharse_date: datetime):
        self.device_id = device_id
        self.device_name = device_name
        self.price = price
        self.purcharse_date = purcharse_date
        self.assigned_to = None
        self.maintenance_history = []

    @abstractmethod
    def get_specs(self) -> dict:
        """Return the specifications of the device."""
        pass


    def assign_to(self, employee_id: str):
        """Assign the device to an employee."""
        self.assigned_to = employee_id
        print(f"Device {self.device_id} assigned to employee {employee_id}.")

    def add_maintenance_log(self, note: str, cost: float):
        log = {
            "date": datetime.now().strftime("%d-%m-%Y"),
            "note": note,
            "cost": cost
        }

        self.maintenance_history.append(log)

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "id": self.device_id,
            "name": self.device_name,
            "assigned_to": self.assigned_to,
            "specs": self.get_specs()
        }
    

    


        