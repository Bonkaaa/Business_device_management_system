from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Tablet(BaseDevice):
    """
    Đại diện cho một tablet trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        screen_size_inches: float,
        battery_life_hours: int,
        has_stylus: bool, # có bút cảm ứng hay không
        operating_system: str
    ):
        """
        Khởi tạo một đối tượng Tablet.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            screen_size_inches (float): Kích thước màn hình tính bằng inch.
            battery_life_hours (int): Thời lượng pin tính bằng giờ.
            has_stylus (bool): Cho biết tablet có bút cảm ứng hay không.
            operating_system (str): Hệ điều hành của tablet.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size_inches = screen_size_inches
        if battery_life_hours <= 0:
            raise ValueError("Battery life must be a positive integer.")
        self._battery_life_hours = battery_life_hours
        self._has_stylus = has_stylus
        self._operating_system = operating_system

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của tablet dưới dạng chuỗi.
        """
        stylus_str = "Có bút cảm ứng" if self._has_stylus else "Không có bút cảm ứng"
        return (
            f"{self._screen_size_inches}\" | Pin: {self._battery_life_hours} giờ | "
            f"{stylus_str} | OS: {self._operating_system}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "screen_size_inches": self._screen_size_inches,
            "battery_life_hours": self._battery_life_hours,
            "has_stylus": self._has_stylus,
            "operating_system": self._operating_system
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem tablet có cần bảo trì hay không.
        """
        return self._battery_life_hours < 5
    
    def __str__(self):
        return f"Tablet(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"