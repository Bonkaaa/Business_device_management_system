from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Printer(BaseDevice):
    """
    Đại diện cho một máy in trong thiết bị của phòng ban.
    """
    def __init__(
    self,
    device_id: str,
    name: str,
    price: float,
    purchase_date: datetime,
    location: str,
    assigned_to: Employee | None,
    print_technology: str,
    ppm: int,
    is_color: bool,
    is_networked: bool,             
) -> None:
        """
        Khởi tạo một đối tượng Printer.
        
        Args:
            device_id (str): ID của thiết bị.
            name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            print_technology (str): Công nghệ in (ví dụ: Laser, Inkjet).
            ppm (int): Số trang in mỗi phút.
            is_color (bool): Cho biết máy in có in màu hay không.
            is_networked (bool): Cho biết máy in có kết nối mạng hay không.
        """
        super().__init__(device_id, name, price, purchase_date, location)
        self._assigned_to = assigned_to

        self._print_technology = print_technology
        if ppm <= 0:
            raise ValueError("PPM must be a positive integer.")
        self._ppm = ppm
        self._is_color = is_color
        self._is_networked = is_networked

    def get_specs(self):
        """
        Trả về các thông số kỹ thuật của máy in dưới dạng chuỗi.
        """
        color_str = "Màu" if self._is_color else "Đen trắng"
        net_str = "Network" if self._is_networked else "USB"
        return f"{self._print_technology} | {color_str} | {self._ppm} trang/phút | {net_str}"
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "print_technology": self._print_technology,
            "ppm": self._ppm,
            "is_color": self._is_color,
            "is_networked": self._is_networked
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem máy in có cần bảo trì hay không.
        """
        return self._ppm < 10
    
    def __str__(self):
        return f"Printer(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
    
