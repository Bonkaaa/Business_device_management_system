from src.base import BaseDevice
from datetime import datetime

class Personal_computer(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        cpu: str,
        ram_gb: int,
        storage_gb: int,
        gpu: str,
        operating_system: str
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        self.cpu = cpu
        if ram_gb <= 0:
            raise ValueError("RAM must be a positive integer.")
        self.ram_gb = ram_gb
        if storage_gb <= 0:
            raise ValueError("Storage must be a positive integer.")
        self.storage_gb = storage_gb
        self.gpu = gpu
        self.operating_system = operating_system

    def get_specs(self) -> str:
        return (
            f"CPU: {self.cpu} | RAM: {self.ram_gb}GB | "
            f"Storage: {self.storage_gb}GB | GPU: {self.gpu} | "
            f"OS: {self.operating_system}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "cpu": self.cpu,
            "ram_gb": self.ram_gb,
            "storage_gb": self.storage_gb,
            "gpu": self.gpu,
            "operating_system": self.operating_system
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.ram_gb < 4 or self.storage_gb < 128
    
    def __str__(self):
        return f"PersonalComputer(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"