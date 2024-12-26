import asyncio
import json

from loguru import logger
from pymavlink import mavutil

from core.controller import Controller
from core.coords import GPSCoords
from core.device import Device
from mavlink.connection import MAVLinkConnection


class MAVLinkController(Controller):
    def __init__(self, device: Device):
        self.connection = MAVLinkConnection(device)

    async def takeoff(self, altitude):
        logger.info("Taking off...")
        self.connection.send(
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            altitude,
        )
        await asyncio.sleep(10)

    async def land(self):
        logger.info("Landing...")
        self.connection.send(
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        await asyncio.sleep(10)

    async def move_to_point(self, coords: GPSCoords):
        logger.info(f"Moving to ({coords.latitude}, {coords.longitude})...")
        self.connection.send(
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            0b0000111111111000,
            coords.latitude,
            coords.longitude,
            -10,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        await asyncio.sleep(5)

    async def log_sensor(self):
        while True:
            msg = self.connection.receive("GLOBAL_POSITION_INT")
            logger.info(
                f"Altitude: {msg.relative_alt / 1000} m, Lat: {msg.lat / 1e7}, Lon: {msg.lon / 1e7}"
            )
            await asyncio.sleep(5)

    async def turn(self, angle: float):
        logger.info(f"Turning to {angle}°")
        self.connection.send(
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            angle,
            0,
            1,
            0,
            0,
            0,
            0,
        )
        await asyncio.sleep(5)

    async def request_lidar_data(self):
        lidar_data = {
            "angles": [0, 30, 60, 90, 120, 150, 180],
            "distances": [1.2, 2.0, 3.5, 0.8, 1.1, 1.5, 2.3],
        }

        logger.info("Getting lidar data...")
        await asyncio.sleep(1)
        return json.dumps(lidar_data)
