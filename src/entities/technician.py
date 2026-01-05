from .employee import Employee
from typing import Dict
from manager import MaintenanceManager
from utils.constant_class import MaintenanceStatus
from .department import Department

class Technician(Employee):
    def __init__(
        self,
        name: str,
        employee_id: str,
        email: str,
        phone_number: str,
        position: str,
        department: Department
    ):
        super().__init__(
            name=name,
            employee_id=employee_id,
            email=email,
            phone_number=phone_number,
            position=position,
            department=department
        )
        
        self.__role = "Technician"

    def inspect_device(self, maintenance_manager: MaintenanceManager, ticket_id: str) -> Dict:
        ticket = maintenance_manager.search_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Phiếu bảo trì với ID {ticket_id} không tồn tại.")
        
        device = ticket.get_device()

        inspection_report = {
            "device_id": device.get_id(),
            "device_name": device.name,
            "reported_by": ticket.get_reporter().name,
            "issue_description": ticket.get_issue_description(),
            "reported_date": ticket.get_issue_description(),
            "current_status": device.get_status(),
            "quality_status": device.get_quality_status(),
            "specifications": device.get_specifications(),
        }

        return inspection_report
    
    def write_technician_notes(self, maintenance_manager: MaintenanceManager, ticket_id: str, notes: str) -> None:
        ticket = maintenance_manager.search_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Phiếu bảo trì với ID {ticket_id} không tồn tại.")
        ticket.technician_notes += f"[Ghi chú kỹ thuật viên] {notes}"



        


        