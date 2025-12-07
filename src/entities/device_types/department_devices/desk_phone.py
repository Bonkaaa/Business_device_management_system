from src.base import BaseDevice
from datetime import datetime
from employee import Employee

class DeskPhone(BaseDevice):
    """
    Đại diện cho một điện thoại bàn trong thiết bị của phòng ban.
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
        support_voip: bool,
    ):
        """
        Khởi tạo một đối tượng DeskPhone.

        Args:
            device_id (str): ID của thiết bị.
            device_name (str): Tên của thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí của thiết bị.
            assigned_to (Employee | None): Nhân viên được giao thiết bị.
            model (str): Mẫu điện thoại bàn.
            support_voip (bool): Cho biết điện thoại có hỗ trợ VoIP hay không.
        """
        super().__init__(device_id, device_name, price, purchase_date, location)
        self._assigned_to = assigned_to

        self.model = model
        self._support_voip = support_voip

    def get_specs(self) -> str:
        """
        Trả về các thông số kỹ thuật của điện thoại bàn dưới dạng chuỗi.
        """
        voip = "Hỗ trợ VoIP" if self._support_voip else "Không hỗ trợ VoIP"
        return f"{self.model} | {voip}"
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "Model": self.model,
            "Support VoIP": self._support_voip
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        """
        Xác định xem điện thoại bàn có cần bảo trì hay không.
        """
        # No specific maintenance criteria for desk phones
        if not self._support_voip:
            return True
    
    def __str__(self):
        return f"DeskPhone(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
        

