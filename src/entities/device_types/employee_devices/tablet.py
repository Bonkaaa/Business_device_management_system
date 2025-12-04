from src.base import BaseDevice
from datetime import datetime

class Tablet(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        screen_size_inches: float,
        battery_life_hours: int,
        has_stylus: bool, # có bút cảm ứng hay không
        operating_system: str
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self.screen_size_inches = screen_size_inches
        if battery_life_hours <= 0:
            raise ValueError("Battery life must be a positive integer.")
        self.battery_life_hours = battery_life_hours
        self.has_stylus = has_stylus
        self.operating_system = operating_system

    def get_specs(self) -> str:
        stylus_str = "Có bút cảm ứng" if self.has_stylus else "Không có bút cảm ứng"
        return (
            f"{self.screen_size_inches}\" | Pin: {self.battery_life_hours} giờ | "
            f"{stylus_str} | OS: {self.operating_system}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "screen_size_inches": self.screen_size_inches,
            "battery_life_hours": self.battery_life_hours,
            "has_stylus": self.has_stylus,
            "operating_system": self.operating_system
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.battery_life_hours < 5
    
    def __str__(self):
        return f"Tablet(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"