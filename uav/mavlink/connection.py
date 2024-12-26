from pymavlink import mavutil

from core.connection import Connection
from core.device import Device


class MAVLinkConnection(Connection):
    def __init__(self, device: Device):
        self.master = mavutil.mavlink_connection(device.address)
        self.target_system = 1
        self.target_component = 1

    def send(self, *args):
        self.master.mav.send(*args)

    def receive(self, msg_type, blocking=True):
        return self.master.recv_match(type=msg_type, blocking=blocking)
