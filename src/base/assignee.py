from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Device

class Assignee(ABC):
    def __init__(
        self,
        name: str,
        assignee_id: str,
    ):
        self._id = assignee_id
        self.name = name

    def get_id(self) -> str:
        return self._id
    
    def get_name(self) -> str:
        return self.name

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