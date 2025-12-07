from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Smartphone(BaseDevice):
    """
    Đại diện cho một điện thoại thông minh trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        os: str,
        storage_gb: int,
        ram_gb: int,
        screen_size_inches: float,
        has_5g: bool
    ):
        """
        Khởi tạo một đối tượng Smartphone.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            os (str): Hệ điều hành của điện thoại.
            storage_gb (int): Dung lượng lưu trữ tính bằng GB.
            ram_gb (int): Dung lượng RAM tính bằng GB.
            screen_size_inches (float): Kích thước màn hình tính bằng inch.
            has_5g (bool): Cho biết điện thoại có hỗ trợ 5G hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        self._os = os
        if storage_gb <= 0:
            raise ValueError("Storage must be a positive integer.")
        self._storage_gb = storage_gb
        if ram_gb <= 0:
            raise ValueError("RAM must be a positive integer.")
        self._ram_gb = ram_gb
        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size_inches = screen_size_inches
        self._has_5g = has_5g

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của điện thoại thông minh dưới dạng chuỗi.
        """
        network_str = "Hỗ trợ 5G" if self._has_5g else "Không hỗ trợ 5G"
        return (
            f"OS: {self._os} | Storage: {self._storage_gb}GB | "
            f"RAM: {self._ram_gb}GB | Màn hình: {self._screen_size_inches}\" | {network_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "os": self._os,
            "storage_gb": self._storage_gb,
            "ram_gb": self._ram_gb,
            "screen_size_inches": self._screen_size_inches,
            "has_5g": self._has_5g
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem điện thoại thông minh có cần bảo trì hay không.
        """
        return self._ram_gb < 2 or self._storage_gb < 32