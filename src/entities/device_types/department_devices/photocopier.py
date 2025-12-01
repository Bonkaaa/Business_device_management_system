from src.base.base_device import BaseDevice
from datetime import datetime

class Photocopier(BaseDevice):
    def __init__(
        self,
        device_id: str,
        name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        copy_speed: int,
        dpi: int,
        is_color: bool,
        paper_capacity: int
    ) -> None:
        super().__init__(device_id, name, price, purchase_date, location)

        self.assigned_to = assigned_to
        if copy_speed <= 0:
            raise ValueError("Copy speed must be a positive integer.")
        self.copy_speed = copy_speed
        self.dpi = dpi
        self.is_color = is_color
        self.paper_capacity = paper_capacity

    def get_specs(self):
        color_str = "Màu" if self.is_color else "Đen trắng"
        return (
            f"{color_str} | {self.copy_speed} trang/phút | "
            f"{self.dpi} DPI | Khay {self.paper_capacity} tờ"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "copy_speed": self.copy_speed,
            "dpi": self.dpi,
            "is_color": self.is_color,
            "paper_capacity": self.paper_capacity
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.copy_speed < 15
    
    def __str__(self):
        return f"Photocopier(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"