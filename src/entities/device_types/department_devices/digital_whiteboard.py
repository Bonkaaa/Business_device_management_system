from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class DigitalWhiteboard(BaseDevice):
    """
    Đại diện cho một bảng trắng kỹ thuật số trong thiết bị của phòng ban.
    """
    def __init__(
        self,
        device_id: str,
        name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        screen_size: float,
        resolution: str,
        touchscreen: bool,
    ) -> None:
        """
        Khởi tạo một đối tượng DigitalWhiteboard.

        Args:
            device_id (str): ID của thiết bị.
            name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            screen_size (float): Kích thước màn hình
        """
        super().__init__(device_id, name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if screen_size <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size = screen_size
        self._resolution = resolution
        self._touchscreen = touchscreen

    def get_specs(self):
        """
        Trả về các thông số kỹ thuật của bảng trắng kỹ thuật số dưới dạng chuỗi.
        """
        touch_str = "Cảm ứng" if self._resolution else "Không cảm ứng"
        return f"{self._screen_size} inch | {self._resolution} | {touch_str}"
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem bảng trắng kỹ thuật số có cần bảo trì hay không.
        """
        return not self._touchscreen
    
    def __str__(self):
        return f"DigitalWhiteboard(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "screen_size": self._screen_size,
            "resolution": self._resolution,
            "touchscreen": self._touchscreen
        })
        return base_dict
        