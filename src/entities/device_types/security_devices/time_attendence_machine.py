from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class TimeAttendenceMachine(BaseDevice):
    """
    Đại diện cho một máy chấm công trong thiết bị an ninh.
    """
    def __init__(
        self,
        device_id: str,
        device_name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        assigned_to: Employee | None,
        model: str,
        manufacturer: str,
        connectivity_type: str,  # e.g., WiFi, Ethernet
        max_users: int,
        supports_fingerprint: bool,
        supports_face_recognition: bool
    ):
        """
        Khởi tạo một đối tượng TimeAttendenceMachine.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            model (str): Mẫu máy chấm công.
            manufacturer (str): Nhà sản xuất.
            connectivity_type (str): Loại kết nối (ví dụ: WiFi, Ethernet).
            max_users (int): Số người dùng tối đa.
            supports_fingerprint (bool): Cho biết có hỗ trợ vân tay hay không.
            supports_face_recognition (bool): Cho biết có hỗ trợ nhận diện khuôn mặt hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to
        
        self._model = model
        self._manufacturer = manufacturer
        self._connectivity_type = connectivity_type
        if max_users <= 0:
            raise ValueError("Max users must be a positive integer.")
        self._max_users = max_users
        self._supports_fingerprint = supports_fingerprint
        self._supports_face_recognition = supports_face_recognition

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của máy chấm công dưới dạng chuỗi.
        """
        fingerprint_str = "Hỗ trợ vân tay" if self._supports_fingerprint else "Không hỗ trợ vân tay"
        face_recog_str = "Hỗ trợ nhận diện khuôn mặt" if self._supports_face_recognition else "Không hỗ trợ nhận diện khuôn mặt"
        return (
            f"Mẫu: {self._model} | Nhà sản xuất: {self._manufacturer} | "
            f"Kết nối: {self._connectivity_type} | Max người dùng: {self._max_users} | "
            f"{fingerprint_str} | {face_recog_str}"
        )  
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "model": self._model,
            "manufacturer": self._manufacturer,
            "connectivity_type": self._connectivity_type,
            "max_users": self._max_users,
            "supports_fingerprint": self._supports_fingerprint,
            "supports_face_recognition": self._supports_face_recognition
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem máy chấm công có cần bảo trì hay không dựa trên số người dùng tối đa và các tính năng hỗ trợ.
        """
        return self._max_users > 500 or not (self._supports_fingerprint or self._supports_face_recognition)
    
    def __str__(self):
        return f"TimeAttendenceMachine(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"