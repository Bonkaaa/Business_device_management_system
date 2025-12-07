from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Projector(BaseDevice):
    def __init__(
        self, 
        device_id: str, 
        device_name: str, 
        price: float, 
        purchase_date: datetime, 
        location: str,
        assigned_to: Employee | None,
        lumens: int,                # độ sáng
        resolution: str,            # ví dụ: "1080p", "4K"
        lamp_hours: int,            # tuổi thọ bóng đèn
        is_portable: bool,

    ):
        """
        Khởi tạo một đối tượng Projector.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            lumens (int): Độ sáng của máy chiếu.
            resolution (str): Độ phân giải của máy chiếu.
            lamp_hours (int): Tuổi thọ bóng đèn của máy chiếu.
            is_portable (bool): Máy chiếu có di động hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if lumens <= 0:
            raise ValueError("Lumens must be a positive integer.")
        self._lumens = lumens
        self._resolution = resolution
        self._lamp_hours = lamp_hours
        self._is_portable = is_portable

    def get_specs(self) -> dict:
        """
        Trả về các thông số kỹ thuật của máy chiếu dưới dạng chuỗi.
        """
        portable_str = "Di động" if self._is_portable else "Cố định"
        return (
            f"{self._lumens} lumens | {self._resolution} | "
            f"{self._lamp_hours} giờ | {portable_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "lumens": self._lumens,
            "resolution": self._resolution,
            "lamp_hours": self._lamp_hours,
            "is_portable": self._is_portable
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem máy chiếu có cần bảo trì hay không.
        """
        return self._lamp_hours > 2000
    
    def __str__(self):
        return f"Projector(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"