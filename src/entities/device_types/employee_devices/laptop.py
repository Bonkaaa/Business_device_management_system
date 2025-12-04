from src.base import BaseDevice
from datetime import datetime

class Laptop(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        ram_size_gb: int,          # dung lượng RAM
        storage_size_gb: int,      # dung lượng lưu trữ
        cpu_model: str,            # mẫu CPU
        gpu_model: str,            # mẫu GPU
        screen_size_inches: float  # kích thước màn hình
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        if ram_size_gb <= 0:
            raise ValueError("RAM size must be a positive integer.")
        self.ram_size_gb = ram_size_gb
        if storage_size_gb <= 0:
            raise ValueError("Storage size must be a positive integer.")
        self.storage_size_gb = storage_size_gb
        self.cpu_model = cpu_model
        self.gpu_model = gpu_model
        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self.screen_size_inches = screen_size_inches
        
    def get_specs(self) -> str:
        return (
            f"{self.ram_size_gb}GB RAM | {self.storage_size_gb}GB Storage | "
            f"CPU: {self.cpu_model} | GPU: {self.gpu_model} | "
            f"{self.screen_size_inches}\" Screen"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "ram_size_gb": self.ram_size_gb,
            "storage_size_gb": self.storage_size_gb,
            "cpu_model": self.cpu_model,
            "gpu_model": self.gpu_model,
            "screen_size_inches": self.screen_size_inches
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.ram_size_gb < 4 or self.storage_size_gb < 128
    
    def __str__(self):
        return f"Laptop(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"