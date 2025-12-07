from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Alarm(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        alarm_type: str,
        is_wireless: bool,
        battery_life_hours: int,
        coverage_area_sq_meters: float # diện tích phủ sóng
    ):
        """
        Khởi tạo một đối tượng Alarm.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            alarm_type (str): Loại hệ thống báo động (ví dụ: "Chống trộm", "Báo cháy").
            is_wireless (bool): Cho biết hệ thống báo động có phải là không dây hay không.
            battery_life_hours (int): Thời lượng pin tính bằng giờ.
            coverage_area_sq_meters (float): Diện tích phủ sóng tính bằng mét vuông.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assinged_to = assigned_to
        
        self._alarm_type = alarm_type
        self._is_wireless = is_wireless
        if battery_life_hours <= 0:
            raise ValueError("Battery life must be a positive integer.")
        self._battery_life_hours = battery_life_hours
        if coverage_area_sq_meters <= 0:
            raise ValueError("Coverage area must be a positive number.")
        self._coverage_area_sq_meters = coverage_area_sq_meters

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của hệ thống báo động dưới dạng chuỗi.
        """
        wireless_str = "Không dây" if self._is_wireless else "Có dây"
        return (
            f"Loại: {self._alarm_type} | {wireless_str} | "
            f"Tuổi thọ pin: {self._battery_life_hours} giờ | "
            f"Khu vực phủ sóng: {self._coverage_area_sq_meters} m²"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "alarm_type": self._alarm_type,
            "is_wireless": self._is_wireless,
            "battery_life_hours": self._battery_life_hours,
            "coverage_area_sq_meters": self._coverage_area_sq_meters
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self._battery_life_hours < 24
    
    def __str__(self):
        return f"Alarm(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"