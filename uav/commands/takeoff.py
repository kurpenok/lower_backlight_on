from core.command import Command
from core.controller import Controller


class TakeoffCommand(Command):
    def __init__(self, controller: Controller, altitude: float):
        self.controller = controller
        self.altitude = altitude

    async def execute(self):
        await self.controller.takeoff(self.altitude)
