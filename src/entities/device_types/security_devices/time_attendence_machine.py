from src.base import BaseDevice
from datetime import datetime

class TimeAttendenceMachine(BaseDevice):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        model: str,
        manufacturer: str,
        connectivity_type: str,  # e.g., WiFi, Ethernet
        max_users: int,
        supports_fingerprint: bool,
        supports_face_recognition: bool
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        
        self.model = model
        self.manufacturer = manufacturer
        self.connectivity_type = connectivity_type
        if max_users <= 0:
            raise ValueError("Max users must be a positive integer.")
        self.max_users = max_users
        self.supports_fingerprint = supports_fingerprint
        self.supports_face_recognition = supports_face_recognition

    def get_specs(self) -> str:
        fingerprint_str = "Hỗ trợ vân tay" if self.supports_fingerprint else "Không hỗ trợ vân tay"
        face_recog_str = "Hỗ trợ nhận diện khuôn mặt" if self.supports_face_recognition else "Không hỗ trợ nhận diện khuôn mặt"
        return (
            f"Mẫu: {self.model} | Nhà sản xuất: {self.manufacturer} | "
            f"Kết nối: {self.connectivity_type} | Max người dùng: {self.max_users} | "
            f"{fingerprint_str} | {face_recog_str}"
        )  
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "model": self.model,
            "manufacturer": self.manufacturer,
            "connectivity_type": self.connectivity_type,
            "max_users": self.max_users,
            "supports_fingerprint": self.supports_fingerprint,
            "supports_face_recognition": self.supports_face_recognition
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        return self.max_users > 500 or not (self.supports_fingerprint or self.supports_face_recognition)
    
    def __str__(self):
        return f"TimeAttendenceMachine(ID: {self.device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"