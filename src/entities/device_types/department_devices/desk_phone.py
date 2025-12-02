from src.base import BaseDevice
from datetime import datetime

class DeskPhone(BaseDevice):
    def __init__(
        self, 
        device_id: str, 
        device_name: str, 
        price: float, 
        purchase_date: datetime, 
        location: str,
        model: str,
        support_voip: bool,
    ):
        super().__init__(device_id, device_name, price, purchase_date, location)
        self.model = model

        self._support_voip = support_voip

    def get_specs(self) -> str:
        voip = "Hỗ trợ VoIP" if self._support_voip else "Không hỗ trợ VoIP"
        return f"{self.model} | {voip}"
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "Model": self.model,
            "Support VoIP": self._support_voip
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        # No specific maintenance criteria for desk phones
        if not self._support_voip:
            return True
    
    def __str__(self):
        return f"DeskPhone(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
        

