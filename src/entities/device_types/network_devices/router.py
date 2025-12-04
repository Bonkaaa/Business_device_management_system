from src.base import BaseDevice
from datetime import datetime

class Router(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        num_ports: int, # Số cổng
        max_speed_mbps: int, # Tốc độ tối đa (Mbps)
        supports_wifi_6: bool,  # Hỗ trợ WiFi 6 hay không
        firmware_version: str # Phiên bản firmware
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        if num_ports <= 0:
            raise ValueError("Number of ports must be a positive integer.")
        self.num_ports = num_ports
        if max_speed_mbps <= 0:
            raise ValueError("Max speed must be a positive integer.")
        self.max_speed_mbps = max_speed_mbps
        self.supports_wifi_6 = supports_wifi_6
        self.firmware_version = firmware_version

    def get_specs(self) -> str:
        wifi_str = "Hỗ trợ WiFi 6" if self.supports_wifi_6 else "Không hỗ trợ WiFi 6"
        return (
            f"{self.num_ports} cổng | {self.max_speed_mbps} Mbps | "
            f"{wifi_str} | Firmware: {self.firmware_version}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "num_ports": self.num_ports,
            "max_speed_mbps": self.max_speed_mbps,
            "supports_wifi_6": self.supports_wifi_6,
            "firmware_version": self.firmware_version
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.max_speed_mbps < 100
    
    def __str__(self):
        return f"Router(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"