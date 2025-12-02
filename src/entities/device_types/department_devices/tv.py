from src.base import BaseDevice
from datetime import datetime

class TV(BaseDevice):
    def __inti__(
        self,
        device_id: str,
        name: str,
        price: float,
        purchase_date: datetime,
        location: str,
        screen_size: float,
        resolution: str,
        display_type: str,
        smart_tv: bool,
    ) -> None:
        super().__init__(device_id, name, price, purchase_date, location)
        if screen_size <= 0:
            raise ValueError("Screen size must be a positive number.")
        self._screen_size = screen_size
        self._resolution = resolution
        self._smart_tv = smart_tv
        self._display_type = display_type

    def get_specs(self):
        smart_str = "Smart TV" if self._smart_tv else "Không phải Smart TV"
        return f"{self._screen_size} inch | {self._resolution} | {self._display_type} | {smart_str}"
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "screen_size": self._screen_size,
            "resolution": self._resolution,
            "display_type": self._display_type,
            "smart_tv": self._smart_tv
        })
        return base_dict
    
    def maintanance_required(self) -> bool:
        pass
    