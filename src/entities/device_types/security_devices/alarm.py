from src.base import BaseDevice
from datetime import datetime

class Alarm(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        alarm_type: str,
        is_wireless: bool,
        battery_life_hours: int,
        coverage_area_sq_meters: float # diện tích phủ sóng
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.alarm_type = alarm_type
        self.is_wireless = is_wireless
        if battery_life_hours <= 0:
            raise ValueError("Battery life must be a positive integer.")
        self.battery_life_hours = battery_life_hours
        if coverage_area_sq_meters <= 0:
            raise ValueError("Coverage area must be a positive number.")
        self.coverage_area_sq_meters = coverage_area_sq_meters

    def get_specs(self) -> str:
        wireless_str = "Không dây" if self.is_wireless else "Có dây"
        return (
            f"Loại: {self.alarm_type} | {wireless_str} | "
            f"Tuổi thọ pin: {self.battery_life_hours} giờ | "
            f"Khu vực phủ sóng: {self.coverage_area_sq_meters} m²"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "alarm_type": self.alarm_type,
            "is_wireless": self.is_wireless,
            "battery_life_hours": self.battery_life_hours,
            "coverage_area_sq_meters": self.coverage_area_sq_meters
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.battery_life_hours < 24
    
    def __str__(self):
        return f"Alarm(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"