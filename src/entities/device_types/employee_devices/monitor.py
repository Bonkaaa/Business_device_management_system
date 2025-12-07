from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Monitor(BaseDevice):
    """
    Đại diện cho một màn hình trong thiết bị của nhân viên.
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
        resolution: str,
        refresh_rate_hz: int,
        is_curved: bool
    ):
        """
        Khởi tạo một đối tượng Monitor.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            screen_size_inches (float): Kích thước màn hình tính bằng inch.
            resolution (str): Độ phân giải của màn hình.
            refresh_rate_hz (int): Tần số quét tính bằng Hz.
            is_curved (bool): Cho biết màn hình có cong hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size_inches = screen_size_inches
        self._resolution = resolution
        if refresh_rate_hz <= 0:
            raise ValueError("Refresh rate must be a positive integer.")
        self._refresh_rate_hz = refresh_rate_hz
        self._is_curved = is_curved

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của màn hình dưới dạng chuỗi."""
        curved_str = "Cong" if self._is_curved else "Phẳng"
        return (
            f"{self._screen_size_inches}\" | {self._resolution} | "
            f"{self._refresh_rate_hz}Hz | {curved_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "screen_size_inches": self._screen_size_inches,
            "resolution": self._resolution,
            "refresh_rate_hz": self._refresh_rate_hz,
            "is_curved": self._is_curved
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem màn hình có cần bảo trì hay không.
        """
        return self._refresh_rate_hz < 60
    
    def __str__(self):
        return f"Monitor(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"