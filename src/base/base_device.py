from abc import ABC, abstractmethod
from datetime import datetime

class BaseDevice(ABC):
    """
    Lớp trừu tượng cơ sở cho tất cả các thiết bị trong hệ thống quản lý thiết bị.
    """
    def __init__(self, device_id: str, device_name: str, price: float, purchase_date: datetime, location: str):
        """
        Khởi tạo một thiết bị cơ sở với các thuộc tính chung.

        Args:
            device_id (str): Mã định danh duy nhất của thiết bị.
            device_name (str): Tên thiết bị.
            price (float): Giá của thiết bị.
            purchase_date (datetime): Ngày mua thiết bị.
            location (str): Vị trí hiện tại của thiết bị.
        """
        # Protected attributes
        self._device_id = device_id
        self._price = price
        self._purchase_date = purchase_date

        # Public attributes
        self.device_name = device_name
        self.location = location
        self._maintenance_history = []

    @abstractmethod
    def get_specs(self) -> dict:
        """Trả về các thông số kỹ thuật của thiết bị dưới dạng Dict."""
        pass


    def add_maintenance_log(self, note: str, cost: float):
        """
        Thêm một bản ghi bảo trì cho thiết bị.
        Args:
            note (str): Ghi chú về bảo trì.
            cost (float): Chi phí bảo trì.
        """
        log = {
            "date": datetime.now().strftime("%d-%m-%Y"),
            "note": note,
            "cost": cost
        }

        self.maintenance_history.append(log)

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "id": self.device_id,
            "name": self.device_name,
            "assigned_to": self.assigned_to,
            "specs": self.get_specs()
        }
    
    @abstractmethod
    def maintanance_required(self) -> bool:
        """Xác định xem thiết bị có cần bảo trì hay không dựa trên các tiêu chí cụ thể của loại thiết bị."""
        pass
    

    


        