#!/usr/bin/env python3

import asyncio
import os

from dotenv import load_dotenv
from loguru import logger

from commands.land import LandCommand
from commands.move_to_point import MoveToPointCommand
from commands.takeoff import TakeoffCommand
from core.coords import GPSCoords
from core.device import Device
from mavlink.controller import MAVLinkController

load_dotenv()
logger.add("drone.log", rotation="1 MB")


async def main() -> None:
    address = os.getenv("DEVICE_ADDRESS")
    if address is None:
        address = "udp:127.0.0.1:14551"

    device = Device(address=address)
    controller = MAVLinkController(device)
    asyncio.create_task(controller.log_sensor())

    await TakeoffCommand(controller, 10).execute()
    await MoveToPointCommand(controller, GPSCoords(latitude=5, longitude=5)).execute()
    await MoveToPointCommand(controller, GPSCoords(latitude=5, longitude=-5)).execute()
    await MoveToPointCommand(controller, GPSCoords(latitude=-5, longitude=-5)).execute()
    await MoveToPointCommand(controller, GPSCoords(latitude=-5, longitude=5)).execute()
    await LandCommand(controller).execute()


if __name__ == "__main__":
    asyncio.run(main())
