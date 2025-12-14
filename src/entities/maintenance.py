from datetime import datetime
from .device import Device
from .employee import Employee
from utils.constant_class import MaintenanceStatus

class MaintenanceTicket:
    def __init__(
        self,
        ticket_id: str,
        issue_description: str,
        cost_estimate: float,
        status: MaintenanceStatus,
        reported_date: datetime,

        device: Device,
        reporter: Employee
    ):
        # Public attributes
        self.ticket_id = ticket_id
        self.device = device
        self.reporter = reporter

        # Protected attributes
        self._issue_description = issue_description
        self._cost_estimate = cost_estimate
        self._status = status
        self._reported_date = reported_date

        self._date_resolved = None
        self.__technician_notes = ""

        self.__technician_notes += f"[Khởi tạo] Vào ngày {reported_date.isoformat()}, phiếu bảo trì {ticket_id} đã được tạo cho thiết bị {device.get_id()} bởi nhân viên {reporter.get_id() - reporter.get_name()} với mô tả sự cố: {issue_description}."

    def update_status(self, new_status: MaintenanceStatus):
        if new_status not in MaintenanceStatus:
            raise ValueError(f"Trạng thái bảo trì không hợp lệ: {new_status}")
        self._status = new_status

    def resolve_ticket(self, technician_notes: str | None = None):
        self._status = MaintenanceStatus.RESOLVED
        self.date_resolved = datetime.now()
        self.technician_notes += f"[Giải quyết] Vào ngày {self.date_resolved.isoformat()}, phiếu bảo trì {self.ticket_id} đã được giải quyết."
        if technician_notes:
            self.technician_notes += f" Ghi chú kỹ thuật viên: {technician_notes}"

    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "issue_description": self._issue_description,
            "cost_estimate": self._cost_estimate,
            "status": self._status.value,
            "reported_date": self._reported_date.isoformat(),
            "date_resolved": self._date_resolved.isoformat() if self._date_resolved else None,
            "technician_notes": self.__technician_notes,
            "device_id": self.device.get_id(),
            "reporter_id": self.reporter.get_id(),
        }

    
