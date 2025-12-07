from datetime import datetime

class MaintenanceTicket:
    def __init__(
        self,
        ticket_id: str,
        device_id: str,
        issue_description: str,
        reported_date: datetime,
        cost_estimate: float = 0.0,
        status: str = "Open"
    ):
        self.ticket_id = ticket_id
        self.device_id = device_id
        self.issue_description = issue_description
        self.reported_date = reported_date
        self.cost_estimate = cost_estimate
        self.status = status

        self.date_completed = None
        self.technician_notes = None

    def resolve_ticket(self, technician_notes: str, date_completed: datetime, cost: float):
        self.technician_notes = technician_notes
        self.date_completed = datetime.now().strftime("%d-%m-%Y")
        self.cost = cost
        self.status = "Closed"

    def __str__(self):
        return f"[{self.status}] Ticket {self.ticket_id} - Device: {self.device_id} - Lỗi: {self.issue_description}"
    
    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "device_id": self.device_id,
            "issue_description": self.issue_description,
            "reported_date": self.reported_date.strftime("%d-%m-%Y"),
            "cost_estimate": self.cost_estimate,
            "status": self.status,
            "date_completed": self.date_completed,
            "technician_notes": self.technician_notes
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        ticket = cls(
            ticket_id=data["ticket_id"],
            device_id=data["device_id"],
            issue_description=data["issue_description"],
            reported_date=datetime.strptime(data["reported_date"], "%d-%m-%Y"),
            cost_estimate=data.get("cost_estimate", 0.0),
            status=data.get("status", "Open")
        )
        ticket.date_completed = data.get("date_completed")
        ticket.technician_notes = data.get("technician_notes", "")
        return ticket
        