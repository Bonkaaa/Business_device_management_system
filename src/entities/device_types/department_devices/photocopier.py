from src.base import BaseDevice
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
        self._copy_speed = copy_speed
        self._dpi = dpi
        self._is_color = is_color
        self._paper_capacity = paper_capacity

    def get_specs(self):
        color_str = "Màu" if self._is_color else "Đen trắng"
        return (
            f"{color_str} | {self._copy_speed} trang/phút | "
            f"{self._dpi} DPI | Khay {self._paper_capacity} tờ"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "copy_speed": self._copy_speed,
            "dpi": self._dpi,
            "is_color": self._is_color,
            "paper_capacity": self._paper_capacity
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self._copy_speed < 15
    
    def __str__(self):
        return f"Photocopier(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"