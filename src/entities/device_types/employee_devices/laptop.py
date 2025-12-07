from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Laptop(BaseDevice):
    """
    Đại diện cho một laptop trong thiết bị của nhân viên.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        ram_size_gb: int,          # dung lượng RAM
        storage_size_gb: int,      # dung lượng lưu trữ
        cpu_model: str,            # mẫu CPU
        gpu_model: str,            # mẫu GPU
        screen_size_inches: float  # kích thước màn hình
    ):
        """
        Khởi tạo một đối tượng Laptop.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            ram_size_gb (int): Dung lượng RAM tính bằng GB.
            storage_size_gb (int): Dung lượng lưu trữ tính bằng GB.
            cpu_model (str): Mẫu CPU của laptop.
            gpu_model (str): Mẫu GPU của laptop.
            screen_size_inches (float): Kích thước màn hình tính bằng inch.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        if ram_size_gb <= 0:
            raise ValueError("RAM size must be a positive integer.")
        self._ram_size_gb = ram_size_gb
        if storage_size_gb <= 0:
            raise ValueError("Storage size must be a positive integer.")
        self._storage_size_gb = storage_size_gb
        self._cpu_model = cpu_model
        self._gpu_model = gpu_model
        if screen_size_inches <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size_inches = screen_size_inches
        
    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của laptop dưới dạng chuỗi.
        """
        return (
            f"{self._ram_size_gb}GB RAM | {self._storage_size_gb}GB Storage | "
            f"CPU: {self._cpu_model} | GPU: {self._gpu_model} | "
            f"{self._screen_size_inches}\" Screen"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "ram_size_gb": self._ram_size_gb,
            "storage_size_gb": self._storage_size_gb,
            "cpu_model": self._cpu_model,
            "gpu_model": self._gpu_model,
            "screen_size_inches": self._screen_size_inches
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem laptop có cần bảo trì hay không.
        """
        return self._ram_size_gb < 4 or self._storage_size_gb < 128
    
    def __str__(self):
        return f"Laptop(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"