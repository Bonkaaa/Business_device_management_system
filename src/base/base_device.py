from abc import ABC, abstractmethod
from datetime import datetime

class BaseDevice(ABC):
    def __init__(self, device_id: str, device_name: str, price: float, purchase_date: datetime, location: str):
        self.device_id = device_id
        self.device_name = device_name
        self.price = price
        self.purchase_date = purchase_date
        self.location = location
        self.maintenance_history = []
        self.status = "Active"

    @abstractmethod
    def get_specs(self) -> dict:
        """Return the specifications of the device."""
        pass


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
    
    @abstractmethod
    def maintanance_required(self) -> bool:
        """Determine if the device requires maintenance."""
        pass
    

    


        