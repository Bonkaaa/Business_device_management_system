from entities import Assignment, Device
from base import Assignee
from datetime import datetime
from utils.id_generators import generate_assignment_id
from utils.constant_class import DeviceQualityStatus, DeviceStatus, AssignmentStatus


class AssignmentManager:
    def __init__(
        self, 
        assignments: dict[str, str] = None,
    ): 
        if assignments is None:
            assignments = {}
        self._assignments = assignments

    def assign_device(
        self,
        device: Device,
        assignee: Assignee,
        expected_return_date: str | None,
        quality_status: DeviceQualityStatus | None
    ):
        assignment_id = generate_assignment_id()
        initial_date = datetime.now()

        new_assignment = Assignment(
            assignment_id=assignment_id,
            initial_date=initial_date,
            expected_return_date=expected_return_date,
            quality_status=quality_status,
            notes="",
            device=device,
            assignee=assignee
        )

        self._assignments[assignment_id] = new_assignment

        device.update_device_status(DeviceStatus.ASSIGNED)
        device.update_assigned_to(assignee.get_id())

        assignee.assign_device(device)

        return new_assignment

    def return_device(
        self,
        assignment_id: str,
        return_quality_status: DeviceQualityStatus,
        actual_return_date: datetime | None = None,
        return_date_today: bool = True,
    ):
        assignment = self._assignments.get(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment with ID {assignment_id} does not exist.")

        assignment.close_assignment(
            return_quality_status=return_quality_status,
            actual_return_date=actual_return_date,
            return_date_today=return_date_today,
        )

    def get_overdue_assignments(self) -> list[Assignment]:
        current_date = datetime.now()
        overdue_assignments = []

        for assignment in self._assignments.values():
            expected_return_date = assignment.get_expected_return_date()
            status = assignment.get_status()

            if expected_return_date < current_date and status == AssignmentStatus.OPEN:
                overdue_assignments.append(assignment)

        return overdue_assignments
    

    def find_assignment_by_device_id(self, device_id: str) -> Assignment | None:
        for assignment in self._assignments.values():
            device = assignment.get_device()

            if device.get_id() == device_id:
                return assignment
        return None



    

        
        

        

