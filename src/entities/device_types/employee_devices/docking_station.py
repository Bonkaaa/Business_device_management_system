from src.base import BaseDevice
from datetime import datetime

class DockingStation(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        port_count: int,            # số cổng kết nối
        supports_4k: bool,          # hỗ trợ 4K hay không
        has_ethernet: bool,         # có cổng Ethernet hay không
        power_delivery_watts: int   # công suất cung cấp điện
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        if port_count <= 0:
            raise ValueError("Port count must be a positive integer.")
        self.port_count = port_count
        self.supports_4k = supports_4k
        self.has_ethernet = has_ethernet
        self.power_delivery_watts = power_delivery_watts

    def get_specs(self) -> str:
        support_4k_str = "Hỗ trợ 4K" if self.supports_4k else "Không hỗ trợ 4K"
        ethernet_str = "Có cổng Ethernet" if self.has_ethernet else "Không có cổng Ethernet"
        return (
            f"{self.port_count} cổng | {support_4k_str} | "
            f"{ethernet_str} | {self.power_delivery_watts}W"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "port_count": self.port_count,
            "supports_4k": self.supports_4k,
            "has_ethernet": self.has_ethernet,
            "power_delivery_watts": self.power_delivery_watts
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.power_delivery_watts < 30
    
    def __str__(self):
        return f"DockingStation(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"