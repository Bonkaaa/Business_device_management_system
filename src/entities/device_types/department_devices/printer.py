from src.base.base_device import BaseDevice
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
        self.print_technology = print_technology
        if ppm <= 0:
            raise ValueError("PPM must be a positive integer.")
        self.ppm = ppm
        self.is_color = is_color
        self.is_networked = is_networked

    def get_specs(self):
        color_str = "Màu" if self.is_color else "Đen trắng"
        net_str = "Network" if self.is_networked else "USB"
        return f"{self.print_technology} | {color_str} | {self.ppm} trang/phút | {net_str}"
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "print_technology": self.print_technology,
            "ppm": self.ppm,
            "is_color": self.is_color,
            "is_networked": self.is_networked
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.ppm < 10
    
    def __str__(self):
        return f"Printer(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
    
