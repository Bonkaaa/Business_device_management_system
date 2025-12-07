from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class TV(BaseDevice):
    """
    Đại diện cho một TV trong thiết bị của phòng ban.
    """
    def __inti__(
        self,
        device_id: str,
        name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        screen_size: float,
        resolution: str,
        display_type: str,
        smart_tv: bool,
    ) -> None:
        """
        Khởi tạo một đối tượng TV.
        
        Args:
            device_id (str): ID của thiết bị.
            name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            screen_size (float): Kích thước
            resolution (str): Độ phân giải
            display_type (str): Loại màn hình
            smart_tv (bool): Cho biết TV có phải Smart TV hay không.
        """

        super().__init__(device_id, name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if screen_size <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size = screen_size
        self._resolution = resolution
        self._smart_tv = smart_tv
        self._display_type = display_type

    def get_specs(self):
        """
        Trả về các thông số kỹ thuật của TV dưới dạng chuỗi.
        """
        smart_str = "Smart TV" if self._smart_tv else "Không phải Smart TV"
        return f"{self._screen_size} inch | {self._resolution} | {self._display_type} | {smart_str}"
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "screen_size": self._screen_size,
            "resolution": self._resolution,
            "display_type": self._display_type,
            "smart_tv": self._smart_tv
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        # TV không cần bảo trì định kỳ
        pass

    def __str__(self):
        return f"TV(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
    