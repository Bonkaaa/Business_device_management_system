from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class Webcam(BaseDevice):
    """
    Đại diện cho một webcam trong thiết bị của nhân viên.
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
        has_microphone: bool,
        field_of_view_degrees: int
    ):
        """
        Khởi tạo một đối tượng Webcam.
        
        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            resolution (str): Độ phân giải của webcam.
            fps (int): Số khung hình trên giây.
            has_microphone (bool): Cho biết webcam có micrô hay không.
            field_of_view_degrees (int): Góc nhìn tính bằng độ.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        self._resolution = resolution
        if fps <= 0:
            raise ValueError("FPS must be a positive integer.")
        self._fps = fps
        self._has_microphone = has_microphone
        if field_of_view_degrees <= 0 or field_of_view_degrees > 180:
            raise ValueError("Field of view must be between 1 and 180 degrees.")
        self._field_of_view_degrees = field_of_view_degrees

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của webcam dưới dạng chuỗi.
        """
        mic_str = "Có mic" if self._has_microphone else "Không có mic"
        return (
            f"{self.resolution} | {self._fps} FPS | "
            f"{mic_str} | FOV: {self._field_of_view_degrees}°"
        )
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "assigned_to": self._assigned_to,
            "resolution": self._resolution,
            "fps": self._fps,
            "has_microphone": self._has_microphone,
            "field_of_view_degrees": self._field_of_view_degrees
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem webcam có cần bảo trì hay không.
        """
        return self.fps < 15
    
    def __str__(self):
        return f"Webcam(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"