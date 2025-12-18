from utils.utils import save_to_json, load_from_json
from entities import Device
from typing import Dict, Any, Bool
from utils.id_generators import generate_device_id
from utils.constant_class import DeviceStatus, DeviceQualityStatus

class Inventory:
    def __init__(self):
        self.__devices = {}

    def add_device(
        self,
        category: str,
        name: str,
        specifications: Dict[str, Any],
    ):
        device_id = generate_device_id()
        new_device = Device(
            device_id=device_id,
            name=name,
            category=category,
            status=DeviceStatus.AVAILABLE,
            purchase_date=None,
            assigned_to=None,
            specifications=specifications,
        )
        self.__devices[device_id] = new_device

        return new_device
    
    def remove_device(self, device_id: str) -> None:
        if device_id in self.__devices:
            del self.__devices[device_id]
        else:
            raise ValueError(f"Thiết bị với ID {device_id} không tồn tại trong kho.")
        
    def get_all_available_devices(self) -> list[Device]:
        return [device for device in self.__devices.values() if device.is_available()]
    
    def get_device_by_id(self, device_id: str) -> Device | None:
        return self.__devices.get(device_id)
    
    def search_device_by_category(self, category: str) -> list[Device]:
        return [
            device for device in self.__devices.values() if device.category == category
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            device_id: device.to_dict() for device_id, device in self.__devices.items()
        }
    
    def filter_devices_by_device_status(self, status: DeviceStatus) -> list[Device]:
        return [
            device for device in self.__devices.values() if device.get_status()["status"] == status
        ]
        
    def check_device_quality_status(self, device_id: str) -> Bool:
        device = self.__devices.get(device_id)
        if device:
            quality_status = device.get_quality_status()
            if quality_status == DeviceQualityStatus.GOOD:
                return True
            return False
        else:
            raise ValueError(f"Thiết bị với ID {device_id} không tồn tại trong kho.")
        
    


    

        