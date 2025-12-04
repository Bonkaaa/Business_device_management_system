from src.base import BaseDevice
from datetime import datetime

class CCTV(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        resolution: str,
        fps: int,
        is_night_vision: bool,
        storage_capacity_gb: int
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.resolution = resolution
        if fps <= 0:
            raise ValueError("FPS must be a positive integer.")
        self.fps = fps
        self.is_night_vision = is_night_vision
        if storage_capacity_gb <= 0:
            raise ValueError("Storage capacity must be a positive integer.")
        self.storage_capacity_gb = storage_capacity_gb

    def get_specs(self) -> str:
        night_vision_str = "Có nhìn ban đêm" if self.is_night_vision else "Không có nhìn ban đêm"
        return (
            f"{self.resolution} | {self.fps} FPS | "
            f"{night_vision_str} | Storage: {self.storage_capacity_gb}GB"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "resolution": self.resolution,
            "fps": self.fps,
            "is_night_vision": self.is_night_vision,
            "storage_capacity_gb": self.storage_capacity_gb
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.storage_capacity_gb < 32
    
    def __str__(self):
        return f"CCTV(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"