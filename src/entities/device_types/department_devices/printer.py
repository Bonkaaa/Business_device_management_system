from src.base import BaseDevice
from datetime import datetime

class Printer(BaseDevice):
    def __init__(
    self,
    device_id: str,
    name: str,
    price: float,
    purchase_date: datetime,
    location: str,
    assigned_to: str,
    print_technology: str,
    ppm: int,
    is_color: bool,
    is_networked: bool,             
) -> None:
        super().__init__(device_id, name, price, purchase_date, location)
        self.assigned_to = assigned_to

        self._print_technology = print_technology
        if ppm <= 0:
            raise ValueError("PPM must be a positive integer.")
        self._ppm = ppm
        self._is_color = is_color
        self._is_networked = is_networked

    def get_specs(self):
        color_str = "Màu" if self._is_color else "Đen trắng"
        net_str = "Network" if self._is_networked else "USB"
        return f"{self._print_technology} | {color_str} | {self._ppm} trang/phút | {net_str}"
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "print_technology": self._print_technology,
            "ppm": self._ppm,
            "is_color": self._is_color,
            "is_networked": self._is_networked
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self._ppm < 10
    
    def __str__(self):
        return f"Printer(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
    
