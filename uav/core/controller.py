from abc import ABC, abstractmethod

from core.coords import GPSCoords


class Controller(ABC):
    @abstractmethod
    async def takeoff(self, altitude: float):
        pass

    @abstractmethod
    async def land(self):
        pass

    @abstractmethod
    async def move_to_point(self, coords: GPSCoords):
        pass

    @abstractmethod
    async def log_sensor(self):
        pass
