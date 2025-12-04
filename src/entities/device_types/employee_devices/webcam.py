from src.base import BaseDevice
from datetime import datetime

class Webcam(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: str,
        resolution: str,
        fps: int,
        has_microphone: bool,
        field_of_view_degrees: int
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.assigned_to = assigned_to
        self.resolution = resolution
        if fps <= 0:
            raise ValueError("FPS must be a positive integer.")
        self.fps = fps
        self.has_microphone = has_microphone
        if field_of_view_degrees <= 0 or field_of_view_degrees > 180:
            raise ValueError("Field of view must be between 1 and 180 degrees.")
        self.field_of_view_degrees = field_of_view_degrees

    def get_specs(self) -> str:
        mic_str = "Có mic" if self.has_microphone else "Không có mic"
        return (
            f"{self.resolution} | {self.fps} FPS | "
            f"{mic_str} | FOV: {self.field_of_view_degrees}°"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self.assigned_to,
            "resolution": self.resolution,
            "fps": self.fps,
            "has_microphone": self.has_microphone,
            "field_of_view_degrees": self.field_of_view_degrees
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.fps < 15
    
    def __str__(self):
        return f"Webcam(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"