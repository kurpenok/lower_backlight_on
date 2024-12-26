import json

from loguru import logger

from core.command import Command
from core.controller import Controller


class FindNearestObstacleCommand(Command):
    def __init__(self, controller: Controller):
        self.controller = controller

    async def execute(self):
        lidar_data = await self.controller.request_lidar_data()
        if lidar_data is None:
            return
        lidar_info = json.loads(lidar_data)

        angles = lidar_info["angles"]
        distances = lidar_info["distances"]

        min_distance = min(distances)
        min_index = distances.index(min_distance)
        min_angle = angles[min_index]

        logger.info(f"Nearest obstacle: {min_distance} m at  angle {min_angle}°")

        if min_distance < 1.0:
            logger.warning("Obstacle too close!")
            new_angle = (min_angle + 30) % 360
            await self.controller.turn(new_angle)
        else:
            logger.info("No obstacles")
