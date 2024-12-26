import asyncio

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
