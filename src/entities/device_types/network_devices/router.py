from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Router(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        num_ports: int, # Số cổng
        max_speed_mbps: int, # Tốc độ tối đa (Mbps)
        supports_wifi_6: bool,  # Hỗ trợ WiFi 6 hay không
        firmware_version: str # Phiên bản firmware
    ):
        """
        Khởi tạo một đối tượng Router.
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            num_ports (int): Số cổng của router.
            max_speed_mbps (int): Tốc độ tối đa tính bằng Mbps.
            supports_wifi_6 (bool): Cho biết router có hỗ trợ WiFi 6 hay không.
            firmware_version (str): Phiên bản firmware của router.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if num_ports <= 0:
            raise ValueError("Number of ports must be a positive integer.")
        self._num_ports = num_ports
        if max_speed_mbps <= 0:
            raise ValueError("Max speed must be a positive integer.")
        self._max_speed_mbps = max_speed_mbps
        self._supports_wifi_6 = supports_wifi_6
        self._firmware_version = firmware_version

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của router dưới dạng chuỗi.
        """
        wifi_str = "Hỗ trợ WiFi 6" if self._supports_wifi_6 else "Không hỗ trợ WiFi 6"
        return (
            f"{self._num_ports} cổng | {self._max_speed_mbps} Mbps | "
            f"{wifi_str} | Firmware: {self._firmware_version}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "num_ports": self._num_ports,
            "max_speed_mbps": self._max_speed_mbps,
            "supports_wifi_6": self._supports_wifi_6,
            "firmware_version": self._firmware_version
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem router có cần bảo trì hay không.
        """
        return self._max_speed_mbps < 100
    
    def __str__(self):
        return f"Router(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"