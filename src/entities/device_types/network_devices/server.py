from src.base import BaseDevice
from datetime import datetime

class Server(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        rack_unit_size: int,
        cpu: str,
        ram_gb: int,
        storage_tb: float,
        operating_system: str,
        is_virtualized: bool
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        if rack_unit_size <= 0:
            raise ValueError("Rack unit size must be a positive integer.")
        self.rack_unit_size = rack_unit_size
        self.cpu = cpu
        if ram_gb <= 0:
            raise ValueError("RAM must be a positive integer.")
        self.ram_gb = ram_gb
        if storage_tb <= 0:
            raise ValueError("Storage must be a positive number.")
        self.storage_tb = storage_tb
        self.operating_system = operating_system
        self.is_virtualized = is_virtualized

    def get_specs(self) -> str:
        virtualized_str = "Virtualized" if self.is_virtualized else "Non-Virtualized"
        return (
            f"{self.rack_unit_size}U | CPU: {self.cpu} | "
            f"RAM: {self.ram_gb}GB | Storage: {self.storage_tb}TB | "
            f"OS: {self.operating_system} | {virtualized_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "rack_unit_size": self.rack_unit_size,
            "cpu": self.cpu,
            "ram_gb": self.ram_gb,
            "storage_tb": self.storage_tb,
            "operating_system": self.operating_system,
            "is_virtualized": self.is_virtualized
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.ram_gb < 16 or self.storage_tb < 1
    
    def __str__(self):
        return f"Server(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"