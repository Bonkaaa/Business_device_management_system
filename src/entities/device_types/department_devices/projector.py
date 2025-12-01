from src.base.base_device import BaseDevice
from datetime import datetime

class Projector(BaseDevice):
    def __init__(
        self, 
        device_id: str, 
        device_name: str, 
        price: float, 
        purchase_date: datetime, 
        location: str,
        assigned_to: str,
        lumens: int,                # độ sáng
        resolution: str,            # ví dụ: "1080p", "4K"
        lamp_hours: int,            # tuổi thọ bóng đèn
        is_portable: bool,

    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        if lumens <= 0:
            raise ValueError("Lumens must be a positive integer.")
        self.lumens = lumens
        self.resolution = resolution
        self.lamp_hours = lamp_hours
        self.is_portable = is_portable

    def get_specs(self) -> dict:
        portable_str = "Di động" if self.is_portable else "Cố định"
        return (
            f"{self.lumens} lumens | {self.resolution} | "
            f"{self.lamp_hours} giờ | {portable_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "lumens": self.lumens,
            "resolution": self.resolution,
            "lamp_hours": self.lamp_hours,
            "is_portable": self.is_portable
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.lamp_hours > 2000
    
    def __str__(self):
        return f"Projector(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"