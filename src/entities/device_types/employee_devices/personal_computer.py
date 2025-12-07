from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Personal_computer(BaseDevice):
    """
    Đại diện cho một máy tính cá nhân trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        cpu: str,
        ram_gb: int,
        storage_gb: int,
        gpu: str,
        operating_system: str
    ):
        """
        Khởi tạo một đối tượng Personal_computer.
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            cpu (str): Mẫu CPU của máy tính.
            ram_gb (int): Dung lượng RAM tính bằng GB.
            storage_gb (int): Dung lượng lưu trữ tính bằng GB.
            gpu (str): Mẫu GPU của máy tính.
            operating_system (str): Hệ điều hành cài đặt trên máy tính.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        self._cpu = cpu
        if ram_gb <= 0:
            raise ValueError("RAM must be a positive integer.")
        self._ram_gb = ram_gb
        if storage_gb <= 0:
            raise ValueError("Storage must be a positive integer.")
        self._storage_gb = storage_gb
        self._gpu = gpu
        self._operating_system = operating_system

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của máy tính cá nhân dưới dạng chuỗi."""
        return (
            f"CPU: {self._cpu} | RAM: {self._ram_gb}GB | "
            f"Storage: {self._storage_gb}GB | GPU: {self._gpu} | "
            f"OS: {self._operating_system}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "cpu": self._cpu,
            "ram_gb": self._ram_gb,
            "storage_gb": self._storage_gb,
            "gpu": self._gpu,
            "operating_system": self._operating_system
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem máy tính cá nhân có cần bảo trì hay không.
        """
        return self._ram_gb < 4 or self._storage_gb < 128
    
    def __str__(self):
        return f"PersonalComputer(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"