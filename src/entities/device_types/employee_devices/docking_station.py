from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class DockingStation(BaseDevice):
    """
    Đại diện cho một trạm kết nối trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        port_count: int,            # số cổng kết nối
        supports_4k: bool,          # hỗ trợ 4K hay không
        has_ethernet: bool,         # có cổng Ethernet hay không
        power_delivery_watts: int   # công suất cung cấp điện
    ):
        """
        Khởi tạo một đối tượng DockingStation.

        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            port_count (int): Số cổng kết nối.
            supports_4k (bool): Cho biết có hỗ trợ 4K hay không.
            has_ethernet (bool): Cho biết có cổng Ethernet hay không.
            power_delivery_watts (int): Công suất cung cấp điện tính bằng watt.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if port_count <= 0:
            raise ValueError("Port count must be a positive integer.")
        self._port_count = port_count
        self._supports_4k = supports_4k
        self._has_ethernet = has_ethernet
        self._power_delivery_watts = power_delivery_watts

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của trạm kết nối dưới dạng chuỗi.
        """
        support_4k_str = "Hỗ trợ 4K" if self._supports_4k else "Không hỗ trợ 4K"
        ethernet_str = "Có cổng Ethernet" if self._has_ethernet else "Không có cổng Ethernet"
        return (
            f"{self._port_count} cổng | {support_4k_str} | "
            f"{ethernet_str} | {self._power_delivery_watts}W"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "port_count": self._port_count,
            "supports_4k": self._supports_4k,
            "has_ethernet": self._has_ethernet,
            "power_delivery_watts": self._power_delivery_watts
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem trạm kết nối có cần bảo trì hay không.
        """
        return self._power_delivery_watts < 30
    
    def __str__(self):
        return f"DockingStation(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"