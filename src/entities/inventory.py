from utils.utils import save_to_json, load_from_json
from device import Device
from typing import Dict, Any

class Inventory:
    def __init__(self):
        self.devices = {}

    def add_device(self, device: Device):
        if not isinstance(device, Device):
            raise TypeError("Chỉ có thể thêm các đối tượng thuộc lớp Device.")
        device_id = device.get_id()
        self.devices.update({device_id: device})

    def remove_device(self, device: Device) -> None:
        device_id = device.get_id()
        if device_id in self.devices:
            self.devices.remove(device_id)
        else:
            raise ValueError("Thiết bị không tồn tại trong kho.")
        
        
    def search_device(self, device) -> Device | None:
        device_id = device.get_id()
        if device_id in self.devices:
            return self.devices[device_id]
        else:
            return None
        
        
    def get_all_available_devices(self) -> list[Device]:
        return [device for device in self.devices.values() if device.is_available()]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            device_id: device.to_dict() for device_id, device in self.devices.items()
        }


    

        