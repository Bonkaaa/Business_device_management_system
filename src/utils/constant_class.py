from enum import Enum
from typing import Dict
from utils.utils import save_to_json, load_from_json

class DeviceStatus(Enum):
    AVAILABLE = "Đang có sẵn"
    ASSIGNED = "Đã được giao"
    MAINTENANCE = "Đang bảo trì"
    OUT_OF_SERVICE = "Ngừng hoạt động"

class DeviceQualityStatus(Enum):
    GOOD = "Tốt"
    BROKEN = "Hỏng"
    RETIRED = "Đã ngừng sử dụng"

class AssignmentStatus(Enum):
    OPEN = "Mở"
    CLOSED = "Đóng"
    OVERDUE = "Quá hạn"

class MaintenanceStatus(Enum):
    REPORTED = "Đã báo cáo"
    RESOLVED = "Đã giải quyết"
    CLOSED = "Đóng"

        
        



