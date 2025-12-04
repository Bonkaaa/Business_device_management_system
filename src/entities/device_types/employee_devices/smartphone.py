from src.base import BaseDevice
from datetime import datetime

class Smartphone(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        os: str,
        storage_gb: int,
        ram_gb: int,
        screen_size_inches: float,
        has_5g: bool
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        self.os = os
        if storage_gb <= 0:
            raise ValueError("Storage must be a positive integer.")
        self.storage_gb = storage_gb
        if ram_gb <= 0:
            raise ValueError("RAM must be a positive integer.")
        self.ram_gb = ram_gb
        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self.screen_size_inches = screen_size_inches
        self.has_5g = has_5g

    def get_specs(self) -> str:
        network_str = "Hỗ trợ 5G" if self.has_5g else "Không hỗ trợ 5G"
        return (
            f"OS: {self.os} | Storage: {self.storage_gb}GB | "
            f"RAM: {self.ram_gb}GB | Màn hình: {self.screen_size_inches}\" | {network_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "os": self.os,
            "storage_gb": self.storage_gb,
            "ram_gb": self.ram_gb,
            "screen_size_inches": self.screen_size_inches,
            "has_5g": self.has_5g
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.ram_gb < 2 or self.storage_gb < 32