from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Photocopier(BaseDevice):
    """
    Đại diện cho một máy photocopy trong thiết bị của phòng ban.
    """
    def __init__(
        self,
        device_id: str,
        name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        copy_speed: int,
        dpi: int,
        is_color: bool,
        paper_capacity: int
    ) -> None:
        """
        Khởi tạo một đối tượng Photocopier.
        
        Args:
            device_id (str): ID của thiết bị.
            name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            copy_speed (int): Tốc độ sao chụp (trang/phút).
            dpi (int): Độ phân giải sao chụp.
            is_color (bool): Cho biết máy có sao chụp màu hay không.
            paper_capacity (int): Sức chứa giấy của khay.
        """
        super().__init__(device_id, name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if copy_speed <= 0:
            raise ValueError("Copy speed must be a positive integer.")
        self._copy_speed = copy_speed
        self._dpi = dpi
        self._is_color = is_color
        self._paper_capacity = paper_capacity

    def get_specs(self):
        """
        Trả về các thông số kỹ thuật của máy photocopy dưới dạng chuỗi.
        """
        color_str = "Màu" if self._is_color else "Đen trắng"
        return (
            f"{color_str} | {self._copy_speed} trang/phút | "
            f"{self._dpi} DPI | Khay {self._paper_capacity} tờ"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "copy_speed": self._copy_speed,
            "dpi": self._dpi,
            "is_color": self._is_color,
            "paper_capacity": self._paper_capacity
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem máy photocopy có cần bảo trì hay không.
        """
        return self._copy_speed < 15
    
    def __str__(self):
        return f"Photocopier(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"