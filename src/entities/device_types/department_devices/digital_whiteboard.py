from src.base import BaseDevice
from datetime import datetime

class DigitalWhiteboard(BaseDevice):
    def __init__(
        self,
        device_id: str,
        name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        screen_size: float,
        resolution: str,
        touchscreen: bool,
    ) -> None:
        super().__init__(device_id, name, price, purchase_date, location)
        if screen_size <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size = screen_size
        self._resolution = resolution
        self._touchscreen = touchscreen

    def get_specs(self):
        touch_str = "Cảm ứng" if self._resolution else "Không cảm ứng"
        return f"{self._screen_size} inch | {self._resolution} | {touch_str}"
    
    def maintanance_required(self) -> bool:
        return not self._touchscreen
    
    def __str__(self):
        return f"DigitalWhiteboard(ID: {self._device_id}, Name: {self.device_name}, Specs: {self.get_specs()})"
        