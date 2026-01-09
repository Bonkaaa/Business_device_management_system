from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Device

class Assignee(ABC):
    def __init__(
        self,
        name: str,
        assignee_id: str,
        assigned_devices: list | None = None
    ):
        self._id = assignee_id
        self.name = name
        self.__assigned_devices = assigned_devices if assigned_devices is not None else []

    def get_id(self) -> str:
        return self._id
    
    def get_name(self) -> str:
        return self.name
    
    def get_assigned_devices(self) -> list:
        return self.__assigned_devices
    
    @abstractmethod
    def get_contact_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def get_assignee_type(self) -> str:
        pass

    @abstractmethod
    def assign_device(self, device: "Device") -> None:
        pass

    @abstractmethod
    def unassign_device(self, device: "Device") -> None:
        pass