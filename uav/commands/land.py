from core.command import Command
from core.controller import Controller


class LandCommand(Command):
    def __init__(self, controller: Controller):
        self.controller = controller

    async def execute(self):
        await self.controller.land()
