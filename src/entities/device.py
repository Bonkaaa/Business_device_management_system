from typing import Any, Dict, Optional
from datetime import datetime
from utils.constant_class import DeviceStatus
from utils.constant import DEVICE_CATEGORY


class Device:
    def __init__(
        self,
        device_id: str, 
        name: str, 
        category: str, 
        status: DeviceStatus,
        purchase_date: datetime,
        assigned_to: Optional[str] | None,
        specifications: Dict[str, Any],
    ):
        # Private attributes
        self.__status = status
        self.__purchase_date = purchase_date
        self.__assigned_to = assigned_to
        self.__specifications = specifications

        # Protected attributes
        self._device_id = device_id

        # Public attributes
        self.name = name

        self.category = self._validate_or_add_category(category)
    
    def get_spec(self):
        return self._specifications
    
    def get_id(self):
        return self._device_id
    
    def _validate_or_add_category(self, category: str):
        if category is None:
            raise ValueError("Danh mục thiết bị không được để trống.")
        
        category = category.lower().strip()

        if category not in DEVICE_CATEGORY:
            DEVICE_CATEGORY.append(category)

        return category

    def get_status(self):
        return {
            "status": self.__status,
            "assigned_to": self.__assigned_to,
        }
    
    def update_status(self, new_status: DeviceStatus, assigned_to: Optional[str] = None):
        self.__status = new_status
        self.__assigned_to = assigned_to

    def is_available(self) -> bool:
        return self.__status == DeviceStatus.AVAILABLE
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "device_id": self._device_id,
            "name": self.name,
            "category": self.category,
            "status": self.__status.value,
            "purchase_date": self.__purchase_date.isoformat(),
            "assigned_to": self.__assigned_to,
            "specifications": self.__specifications,
        }
    
    def update_status_and_assignee(
        self,
        new_status: DeviceStatus,
        assigned_to: Optional[str] = None,
    ):
        self.__status = new_status
        self.__assigned_to = assigned_to
    
    

    
    

