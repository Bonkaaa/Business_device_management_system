from typing import Any, Dict, Optional
from datetime import datetime
from utils.constant_class import DeviceStatus, DeviceQualityStatus
from base import Assignee
from utils.constant import DEVICE_CATEGORY


class Device:
    def __init__(
        self,
        device_id: str, 
        name: str, 
        category: str, 
        status: DeviceStatus,
        purchase_date: datetime,
        assigned_to: Assignee | None,
        specifications: Dict[str, Any],
    ):
        # Private attributes
        self.__status = status
        self.__purchase_date = purchase_date
        self.__assigned_to = assigned_to
        self.__specifications = specifications
        self.__device_quality_status = DeviceQualityStatus.GOOD

        # Protected attributes
        self._device_id = device_id

        # Public attributes
        self.name = name

        self.category = self.__validate_or_add_category(category)
    
    def get_spec(self) -> Dict[str, Any]:
        return self._specifications
    
    def get_id(self) -> str:
        return self._device_id
    
    def get_category(self) -> str:
        return self.category
    
    def get_quality_status(self) -> DeviceQualityStatus:
        return self.__device_quality_status
    
    def get_specifications(self) -> Dict[str, Any]:
        return self.__specifications
    
    def __validate_or_add_category(self, category: str) -> str:
        if category is None:
            raise ValueError("Danh mục thiết bị không được để trống.")
        
        category = category.lower().strip()

        if category not in DEVICE_CATEGORY:
            DEVICE_CATEGORY.append(category)

        return category

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self.__status,
            "assigned_to": self.__assigned_to,
        }

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

    def update_device_status(
        self,
        new_status: DeviceStatus,
    ):
        self.__status = new_status
    
    def update_assigned_to(
        self,
        assigned_to: Assignee,
    ):
        self.__assigned_to = assigned_to

    def update_quality_status(
        self,
        new_quality_status: DeviceQualityStatus,
    ):
        self.__device_quality_status = new_quality_status

    
    

    
    

