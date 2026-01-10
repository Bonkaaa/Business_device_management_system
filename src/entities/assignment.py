from datetime import datetime
from utils.constant_class import DeviceStatus, DeviceQualityStatus
from .device import Device
from base import Assignee
from utils.constant_class import AssignmentStatus

class Assignment:
    def __init__(
        self,
        assignment_id: str,
        initial_date: datetime,
        expected_return_date: datetime | None,
        actual_return_date: datetime | None,
        status: AssignmentStatus | None,
        notes: str | None,

        device: Device,
        assignee: Assignee
    ):
        # Private attributes
        self.__initial_date = initial_date
        self.__expected_return_date = expected_return_date
        self.__actual_return_date = actual_return_date


        # Protected attributes
        self._assignment_id = assignment_id
        self._notes = notes
        self._device = device
        self._assignee = assignee

        self._notes += f"[Khởi tạo] Vào ngày {initial_date.isoformat()}, thiết bị {assignment_id} đã được giao cho người dùng/phòng ban {assignee.get_id()} - {assignee.name}."
        self.__status = status if status is not None else AssignmentStatus.OPEN

        if self._device is not None:
            self.__quality_status = self._device.get_status()["status"]
        else:
            self.__quality_status = None

    def get_id(self) -> str:
        return self._assignment_id
    
    def get_expected_return_date(self) -> datetime:
        return self.__expected_return_date
    
    def get_status(self) -> AssignmentStatus:
        return self.__status
    
    def get_device(self) -> Device:
        return self._device
    
    def get_notes(self) -> str:
        return self._notes
    
    def get_initial_date(self) -> datetime:
        return self.__initial_date
    
    def get_assignee(self) -> Assignee:
        return self._assignee
    
    def get_actual_return_date(self) -> datetime | None:
        return self.__actual_return_date if hasattr(self, '_Assignment__actual_return_date') else None
    
    def update_status(self, new_status: AssignmentStatus):
        self.__status = new_status
    
    def to_dict(self) -> dict:
        device_id = self._device.get_id()
        assignee_id = self._assignee.get_id()

        return {
            "assignment_id": self._assignment_id,
            "initial_date": self.__initial_date.isoformat(),
            "expected_return_date": self.__expected_return_date.isoformat() if self.__expected_return_date else None,
            "actual_return_date": self.__actual_return_date.isoformat() if hasattr(self, '_Assignment__actual_return_date') and self.__actual_return_date else None,
            "return_quality_status": self.__return_quality_status.value if hasattr(self, '_Assignment__return_quality_status') and self.__return_quality_status else None,
            "quality_status": self.__quality_status.value if self.__quality_status else None,
            "notes":  self._notes,
            "device_id": device_id,
            "assignee_id": assignee_id,
            "status": self.__status.value,
        }
    
    def return_device(
        self,
        return_quality_status: DeviceQualityStatus,
        actual_return_date: datetime | None = None,
        return_date_today: bool = False,
        broken_status: bool = False,
    ):
        self.__return_quality_status = return_quality_status

        # Check if actual_return_date is provided or if return_date_today is True
        if return_date_today:
            self.__actual_return_date = datetime.now()
        else:
            self.__actual_return_date = actual_return_date

        # Check overdue or not
        if self.__expected_return_date is not None and actual_return_date > self.__expected_return_date:
            self.__status = AssignmentStatus.OVERDUE
        else:
            self.__status = AssignmentStatus.CLOSED

        # Update device status and quality status and assignee
        if broken_status:
            self._device.update_device_status(DeviceStatus.OUT_OF_SERVICE)
        else:
            self._device.update_device_status(DeviceStatus.AVAILABLE)

        self._device.update_quality_status(return_quality_status)
        self._device.update_assigned_to(None)

        # Remove device from assignee's list
        self._assignee.unassign_device(self._device.get_id())


        # Update notes
        self._notes += f"[Đóng] Vào ngày {self.__actual_return_date.isoformat() if self.__actual_return_date else 'N/A'}, thiết bị {self._device.get_id()} đã được trả về với tình trạng chất lượng: {self.__return_quality_status}."


        


        
        
        
        