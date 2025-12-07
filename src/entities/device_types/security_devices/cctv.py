from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class CCTV(BaseDevice):
    """
    Đại diện cho một camera giám sát (CCTV) trong thiết bị an ninh.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        resolution: str,
        fps: int,
        is_night_vision: bool,
        storage_capacity_gb: int
    ):
        """
        Khởi tạo một đối tượng CCTV.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            resolution (str): Độ phân giải của CCTV.
            fps (int): Số khung hình trên giây.
            is_night_vision (bool): Cho biết CCTV có chức năng nhìn ban đêm hay không.
            storage_capacity_gb (int): Dung lượng lưu trữ tính bằng GB.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to
        
        self._resolution = resolution
        if fps <= 0:
            raise ValueError("FPS must be a positive integer.")
        self._fps = fps
        self._is_night_vision = is_night_vision
        if storage_capacity_gb <= 0:
            raise ValueError("Storage capacity must be a positive integer.")
        self._storage_capacity_gb = storage_capacity_gb

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của CCTV dưới dạng chuỗi.
        """
        night_vision_str = "Có nhìn ban đêm" if self._is_night_vision else "Không có nhìn ban đêm"
        return (
            f"{self._resolution} | {self._fps} FPS | "
            f"{night_vision_str} | Storage: {self._storage_capacity_gb}GB"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "resolution": self._resolution,
            "fps": self._fps,
            "is_night_vision": self._is_night_vision,
            "storage_capacity_gb": self._storage_capacity_gb
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem CCTV có cần bảo trì hay không dựa trên dung lượng lưu trữ.
        """
        return self._storage_capacity_gb < 32
    
    def __str__(self):
        return f"CCTV(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"