from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Mouse(BaseDevice):
    """
    Đại diện cho một chuột trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        dpi: int,                    # độ nhạy
        is_wireless: bool,          # không dây hay có dây
        number_of_buttons: int,     # số nút bấm
        has_rgb_lighting: bool      # có đèn RGB hay không
    ):
        """
        Khởi tạo một đối tượng Mouse.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            dpi (int): Độ nhạy của chuột.
            is_wireless (bool): Cho biết chuột có phải là không dây hay không.
            number_of_buttons (int): Số nút bấm trên chuột.
            has_rgb_lighting (bool): Cho biết chuột có đèn RGB hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if dpi <= 0:
            raise ValueError("DPI must be a positive integer.")
        self._dpi = dpi
        self._is_wireless = is_wireless
        if number_of_buttons <= 0:
            raise ValueError("Number of buttons must be a positive integer.")
        self._number_of_buttons = number_of_buttons
        self._has_rgb_lighting = has_rgb_lighting

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của chuột dưới dạng chuỗi.
        """
        wireless_str = "Không dây" if self._is_wireless else "Có dây"
        rgb_str = "Có RGB" if self._has_rgb_lighting else "Không RGB"
        return (
            f"{self._dpi} DPI | {wireless_str} | "
            f"{self._number_of_buttons} nút | {rgb_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "dpi": self._dpi,
            "is_wireless": self._is_wireless,
            "number_of_buttons": self._number_of_buttons,
            "has_rgb_lighting": self._has_rgb_lighting
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem chuột có cần bảo trì hay không.
        """
        return self.dpi < 800
    
    def __str__(self):
        return f"Mouse(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"