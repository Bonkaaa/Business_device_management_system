from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Keyboard(BaseDevice):
    """
    Đại diện cho một bàn phím trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        is_mechanical: bool,        # cơ học hay không
        key_switch_type: str,       # loại switch (nếu cơ học)
        backlight_color: str,       # màu đèn nền
        has_numpad: bool            # có bàn phím số hay không
    ):
        """
        Khởi tạo một đối tượng Keyboard.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            is_mechanical (bool): Cho biết bàn phím có phải là cơ học hay không.
            key_switch_type (str): Loại switch nếu là bàn phím cơ học.
            backlight_color (str): Màu đèn nền của bàn phím.
            has_numpad (bool): Cho biết bàn phím có bàn phím số hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        self._is_mechanical = is_mechanical
        self._key_switch_type = key_switch_type if is_mechanical else "N/A"
        self._backlight_color = backlight_color
        self._has_numpad = has_numpad

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của bàn phím dưới dạng chuỗi.
        """
        mechanical_str = "Cơ học" if self._is_mechanical else "Không cơ học"
        numpad_str = "Có bàn phím số" if self._has_numpad else "Không có bàn phím số"
        return (
            f"{mechanical_str} | Switch: {self._key_switch_type} | "
            f"Đèn nền: {self._backlight_color} | {numpad_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "is_mechanical": self._is_mechanical,
            "key_switch_type": self._key_switch_type,
            "backlight_color": self._backlight_color,
            "has_numpad": self._has_numpad
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem bàn phím có cần bảo trì hay không.
        """
        return self._is_mechanical and self._key_switch_type.lower() == "mòn"
    
    def __str__(self):
        return f"Keyboard(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"