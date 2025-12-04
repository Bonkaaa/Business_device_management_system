from src.base import BaseDevice
from datetime import datetime

class Keyboard(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        is_mechanical: bool,        # cơ học hay không
        key_switch_type: str,       # loại switch (nếu cơ học)
        backlight_color: str,       # màu đèn nền
        has_numpad: bool            # có bàn phím số hay không
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        self.is_mechanical = is_mechanical
        self.key_switch_type = key_switch_type if is_mechanical else "N/A"
        self.backlight_color = backlight_color
        self.has_numpad = has_numpad

    def get_specs(self) -> str:
        mechanical_str = "Cơ học" if self.is_mechanical else "Không cơ học"
        numpad_str = "Có bàn phím số" if self.has_numpad else "Không có bàn phím số"
        return (
            f"{mechanical_str} | Switch: {self.key_switch_type} | "
            f"Đèn nền: {self.backlight_color} | {numpad_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "is_mechanical": self.is_mechanical,
            "key_switch_type": self.key_switch_type,
            "backlight_color": self.backlight_color,
            "has_numpad": self.has_numpad
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.is_mechanical and self.key_switch_type.lower() == "mòn"
    
    def __str__(self):
        return f"Keyboard(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"