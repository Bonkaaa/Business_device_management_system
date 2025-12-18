from enum import Enum
from typing import Dict
from utils.utils import save_to_json, load_from_json

class DeviceStatus(Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"

class DeviceQualityStatus(Enum):
    GOOD = "good"
    BROKEN = "broken"
    RETIRED = "retired"

class AssignmentStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    OVERDUE = "overdue"

class MaintenanceStatus(Enum):
    REPORTED = "reported"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "CLOSED"

        
        



