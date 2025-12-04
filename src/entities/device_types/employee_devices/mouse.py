from src.base import BaseDevice
from datetime import datetime

class Mouse(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        dpi: int,                    # độ nhạy
        is_wireless: bool,          # không dây hay có dây
        number_of_buttons: int,     # số nút bấm
        has_rgb_lighting: bool      # có đèn RGB hay không
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        if dpi <= 0:
            raise ValueError("DPI must be a positive integer.")
        self.dpi = dpi
        self.is_wireless = is_wireless
        if number_of_buttons <= 0:
            raise ValueError("Number of buttons must be a positive integer.")
        self.number_of_buttons = number_of_buttons
        self.has_rgb_lighting = has_rgb_lighting

    def get_specs(self) -> str:
        wireless_str = "Không dây" if self.is_wireless else "Có dây"
        rgb_str = "Có RGB" if self.has_rgb_lighting else "Không RGB"
        return (
            f"{self.dpi} DPI | {wireless_str} | "
            f"{self.number_of_buttons} nút | {rgb_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "dpi": self.dpi,
            "is_wireless": self.is_wireless,
            "number_of_buttons": self.number_of_buttons,
            "has_rgb_lighting": self.has_rgb_lighting
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.dpi < 800
    
    def __str__(self):
        return f"Mouse(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"