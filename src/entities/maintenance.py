from datetime import datetime
from .device import Device
from .employee import Employee
from utils.constant_class import MaintenanceStatus

class MaintenanceTicket:
    def __init__(
        self,
        ticket_id: str,
        issue_description: str,
        status: MaintenanceStatus,
        reported_date: datetime,

        device: Device,
        reporter: Employee
    ):
        # Public attributes
        self._ticket_id = ticket_id  
        self._device = device
        self._reporter = reporter

        # Protected attributes
        self._issue_description = issue_description
        self._status = status
        self._reported_date = reported_date

        self.__date_resolved = None
        self.__technician_notes = ""

        self.__technician_notes += f"[Khởi tạo] Vào ngày {reported_date.isoformat()}, phiếu bảo trì {ticket_id} đã được tạo cho thiết bị {device.get_id()} bởi nhân viên {reporter.get_id() - reporter.get_name()} với mô tả sự cố: {issue_description}."

    def update_status(self, new_status: MaintenanceStatus):
        if new_status not in MaintenanceStatus:
            raise ValueError(f"Trạng thái bảo trì không hợp lệ: {new_status}")
        self._status = new_status

    def resolve_ticket(
        self, 
        technician_notes: str | None = None, 
        costs: float | None = None
    ):
        self._status = MaintenanceStatus.RESOLVED
        self.date_resolved = datetime.now()
        self.technician_notes += f"[Giải quyết] Vào ngày {self.date_resolved.isoformat()}, phiếu bảo trì {self._ticket_id} đã được giải quyết. Tiền công: {costs if costs is not None else 'N/A'}."
        if technician_notes:
            self.technician_notes += f" Ghi chú kỹ thuật viên: {technician_notes}"

    def to_dict(self) -> dict:
        return {
            "ticket_id": self._ticket_id,
            "issue_description": self._issue_description,
            "status": self._status.value,
            "reported_date": self._reported_date.isoformat(),
            "date_resolved": self.__date_resolved.isoformat() if self.__date_resolved else None,
            "technician_notes": self.__technician_notes,
            "device_id": self._device.get_id(),
            "reporter_id": self._reporter.get_id(),
        }
    
    def get_id(self) -> str:
        return self._ticket_id
    
    def get_status(self) -> MaintenanceStatus:
        return self._status
    
    def get_reported_date(self) -> datetime:
        return self._reported_date
    
    def get_issue_description(self) -> str:
        return self._issue_description
    
    def get_device(self) -> Device:
        return self._device
    
    def get_reporter(self) -> Employee:
        return self._reporter
    

    
