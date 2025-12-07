from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Server(BaseDevice):
    """
    Đại diện cho một máy chủ trong thiết bị mạng.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        rack_unit_size: int,
        cpu: str,
        ram_gb: int,
        storage_tb: float,
        operating_system: str,
        is_virtualized: bool
    ):
        """
        Khởi tạo một đối tượng Server.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            rack_unit_size (int): Kích thước đơn vị giá đỡ (U).
            cpu (str): Mẫu CPU của máy chủ.
            ram_gb (int): Dung lượng RAM tính bằng GB.
            storage_tb (float): Dung lượng lưu trữ tính bằng TB.
            operating_system (str): Hệ điều hành cài đặt trên máy chủ.
            is_virtualized (bool): Cho biết máy chủ có được ảo hóa hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to
        
        if rack_unit_size <= 0:
            raise ValueError("Rack unit size must be a positive integer.")
        self._rack_unit_size = rack_unit_size
        self._cpu = cpu
        if ram_gb <= 0:
            raise ValueError("RAM must be a positive integer.")
        self._ram_gb = ram_gb
        if storage_tb <= 0:
            raise ValueError("Storage must be a positive number.")
        self._storage_tb = storage_tb
        self._operating_system = operating_system
        self._is_virtualized = is_virtualized

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của máy chủ dưới dạng chuỗi.
        """
        virtualized_str = "Virtualized" if self._is_virtualized else "Non-Virtualized"
        return (
            f"{self._rack_unit_size}U | CPU: {self._cpu} | "
            f"RAM: {self._ram_gb}GB | Storage: {self._storage_tb}TB | "
            f"OS: {self._operating_system} | {virtualized_str}"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "rack_unit_size": self._rack_unit_size,
            "cpu": self._cpu,
            "ram_gb": self._ram_gb,
            "storage_tb": self._storage_tb,
            "operating_system": self._operating_system,
            "is_virtualized": self._is_virtualized
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self._ram_gb < 16 or self._storage_tb < 1
    
    def __str__(self):
        return f"Server(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"