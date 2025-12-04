from src.base import BaseDevice
from datetime import datetime

class HeadSet(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        is_wireless: bool,          # có dây hay không dây
        battery_life_hours: int,    # thời lượng pin (nếu không dây)
        noise_cancellation: bool,   # có chống ồn hay không
        microphone_quality: str     # chất lượng micro (ví dụ: "Cao", "Trung bình", "Thấp")
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        self.is_wireless = is_wireless
        if is_wireless and battery_life_hours <= 0:
            raise ValueError("Battery life must be a positive integer for wireless headsets.")
        self.battery_life_hours = battery_life_hours
        self.noise_cancellation = noise_cancellation
        self.microphone_quality = microphone_quality

    def get_specs(self) -> str:
        wireless_str = "Không dây" if self.is_wireless else "Có dây"
        noise_cancel_str = "Có chống ồn" if self.noise_cancellation else "Không chống ồn"
        battery_str = f"{self.battery_life_hours} giờ pin" if self.is_wireless else "N/A"
        return (
            f"{wireless_str} | {battery_str} | "
            f"{noise_cancel_str} | Mic: {self.microphone_quality}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "is_wireless": self.is_wireless,
            "battery_life_hours": self.battery_life_hours,
            "noise_cancellation": self.noise_cancellation,
            "microphone_quality": self.microphone_quality
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.is_wireless and self.battery_life_hours < 5
    
    def __str__(self):
        return f"Headset(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"