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
        purchase_date: str,
        specifications: Dict[str, Any],
        quality_status: DeviceQualityStatus | None = None,
        assignment_manager= None,
    ):
        # Private attributes
        self.__status = status
        self.__purchase_date = purchase_date
        self.__specifications = specifications
        if quality_status is not None:
            self.__device_quality_status = quality_status
        else:
            self.__device_quality_status = DeviceQualityStatus.GOOD

        # Protected attributes
        self._device_id = device_id
        self._assignment_manager = assignment_manager

        # Public attributes
        self.name = name

        # Convert date string to date object
        self.__purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").date()


        self.category = self.__validate_or_add_category(category)
    
    def get_spec(self) -> Dict[str, Any]:
        return self.__specifications
    
    def get_id(self) -> str:
        return self._device_id
    
    def get_category(self) -> str:
        return self.category
    
    def get_quality_status(self) -> DeviceQualityStatus:
        return self.__device_quality_status
    
    def get_specifications(self) -> Dict[str, Any]:
        return self.__specifications
    
    def get_purchase_date(self) -> str:
        return self.__purchase_date.isoformat()
    
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
            "specifications": self.__specifications,
        }

    def update_device_status(
        self,
        new_status: DeviceStatus,
    ):
        self.__status = new_status

    def update_quality_status(
        self,
        new_quality_status: DeviceQualityStatus,
    ):
        self.__device_quality_status = new_quality_status

    def get_assignee(self) -> Optional[Assignee]:
        if self._assignment_manager:
            assignment = self._assignment_manager.get_active_assignment_by_device_id(self._device_id)

            if assignment:
                return assignment.get_assignee()
            else:
                return None
        return None

    
    

    
    

