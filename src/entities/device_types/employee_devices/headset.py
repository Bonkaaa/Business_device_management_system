from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class HeadSet(BaseDevice):
    """
    Đại diện cho một tai nghe trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        is_wireless: bool,          # có dây hay không dây
        battery_life_hours: int,    # thời lượng pin (nếu không dây)
        noise_cancellation: bool,   # có chống ồn hay không
        microphone_quality: str     # chất lượng micro (ví dụ: "Cao", "Trung bình", "Thấp")
    ):
        """
        Khởi tạo một đối tượng HeadSet.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            is_wireless (bool): Cho biết tai nghe có dây hay không dây.
            battery_life_hours (int): Thời lượng pin tính bằng giờ (nếu không dây).
            noise_cancellation (bool): Cho biết tai nghe có chống ồn hay không.
            microphone_quality (str): Chất lượng micro.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        self._is_wireless = is_wireless
        if is_wireless and battery_life_hours <= 0:
            raise ValueError("Battery life must be a positive integer for wireless headsets.")
        self._battery_life_hours = battery_life_hours
        self._noise_cancellation = noise_cancellation
        self._microphone_quality = microphone_quality

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của tai nghe dưới dạng chuỗi.
        """
        wireless_str = "Không dây" if self._is_wireless else "Có dây"
        noise_cancel_str = "Có chống ồn" if self._noise_cancellation else "Không chống ồn"
        battery_str = f"{self._battery_life_hours} giờ pin" if self._is_wireless else "N/A"
        return (
            f"{wireless_str} | {battery_str} | "
            f"{noise_cancel_str} | Mic: {self._microphone_quality}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "is_wireless": self._is_wireless,
            "battery_life_hours": self._battery_life_hours,
            "noise_cancellation": self._noise_cancellation,
            "microphone_quality": self._microphone_quality
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem tai nghe có cần bảo trì hay không.
        """
        return self._is_wireless and self._battery_life_hours < 5
    
    def __str__(self):
        return f"Headset(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"