from entities import MaintenanceTicket
from utils.constant_class import MaintenanceStatus
from utils.utils import load_json_data, save_json_data
from entities import Device, Employee
from utils.id_generators import generate_maintenance_ticket_id
from utils.constant_class import DeviceStatus, DeviceQualityStatus
from datetime import datetime


class MaintenanceManager:
    def __init__(
        self,
        tickets: dict[str, MaintenanceTicket] = None,
    ):
        if tickets is None:
            tickets = {}
        self.__tickets = tickets

    def create_ticket(
        self,
        issue_description: str,
        device: Device,
        reporter: Employee,
    ) -> MaintenanceTicket:
        ticket_id = generate_maintenance_ticket_id()
        reported_date = datetime.now()

        new_ticket = MaintenanceTicket(
            ticket_id=ticket_id,
            issue_description=issue_description,
            status=MaintenanceStatus.REPORTED,
            reported_date=reported_date,
            device=device,
            reporter=reporter
        )

        self.__tickets[ticket_id] = new_ticket

        # Update device status and quality status
        device.update_device_status(DeviceStatus.MAINTENANCE)
        device.update_quality_status(DeviceQualityStatus.BROKEN)

        return new_ticket
    
    def resolve_ticket(
        self,
        ticket_id: str,
        technician_notes: str | None = None,
        costs: float | None = None
    ):
        ticket = self.__tickets.get(ticket_id)
        if not ticket:
            raise ValueError(f"Phiếu bảo trì với ID {ticket_id} không tồn tại.")

        ticket.resolve_ticket(
            technician_notes=technician_notes,
            costs=costs
        )

    def close_ticket(
        self,
        ticket_id: str,
        is_repaired: bool,
    ):
        ticket = self.__tickets.get(ticket_id)

        device = ticket.get_device()

        if is_repaired:
            device.update_device_status(DeviceStatus.ASSIGNED)
            device.update_quality_status(DeviceQualityStatus.GOOD)

            ticket.update_status(MaintenanceStatus.CLOSED)

        else:
            assignment = self.find_assignment_by_device_id(device.get_id())
            if assignment:
                assignment.return_device(
                    return_quality_status=DeviceQualityStatus.BROKEN,
                    return_date_today=True,
                    broken_status=True
                )
            else:
                device.update_device_status(DeviceStatus.OUT_OF_SERVICE)
                device.update_quality_status(DeviceQualityStatus.BROKEN)

        ticket.update_status(MaintenanceStatus.CLOSED)


    # def search_tickets_by_device_id(
    #     self,
    #     device_id: str,
    #     status_filter: MaintenanceStatus | None = None
    # ) -> list[MaintenanceTicket]:
    #     results = []
    #     for ticket in self.__tickets.values():
    #         if ticket.device.get_id() == device_id:
    #             if status_filter and ticket.get_status() == status_filter:
    #                 results.append(ticket)
    #     return results

    def search_ticket_by_id(self, ticket_id: str) -> MaintenanceTicket | None:
        return self.__tickets.get(ticket_id)
        



    

    
    

    