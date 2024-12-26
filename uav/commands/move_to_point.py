from core.command import Command
from core.controller import Controller
from core.coords import GPSCoords


class MoveToPointCommand(Command):
    def __init__(self, controller: Controller, coords: GPSCoords):
        self.controller = controller
        self.coords = coords

    async def execute(self):
        await self.controller.move_to_point(self.coords)
