from src.base import BaseDevice
from datetime import datetime

class Monitor(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        screen_size_inches: float,
        resolution: str,
        refresh_rate_hz: int,
        is_curved: bool
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self.screen_size_inches = screen_size_inches
        self.resolution = resolution
        if refresh_rate_hz <= 0:
            raise ValueError("Refresh rate must be a positive integer.")
        self.refresh_rate_hz = refresh_rate_hz
        self.is_curved = is_curved

    def get_specs(self) -> str:
        curved_str = "Cong" if self.is_curved else "Phẳng"
        return (
            f"{self.screen_size_inches}\" | {self.resolution} | "
            f"{self.refresh_rate_hz}Hz | {curved_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "screen_size_inches": self.screen_size_inches,
            "resolution": self.resolution,
            "refresh_rate_hz": self.refresh_rate_hz,
            "is_curved": self.is_curved
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.refresh_rate_hz < 60
    
    def __str__(self):
        return f"Monitor(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"