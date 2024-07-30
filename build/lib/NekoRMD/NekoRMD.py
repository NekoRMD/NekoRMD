from NekoRMD.Control import Control
from NekoRMD.MotorInterface import MotorInterface
from NekoRMD.MotorType import MotorType
from NekoRMD.Telemetry import Telemetry
from NekoRMD.MotorLogs import MotorLogs
from NekoRMD.ican import I_CAN
import time


class NekoRMD(MotorInterface):
    def __init__(self, address, motor_type):
        if not isinstance(motor_type, MotorType):
            raise ValueError("Invalid motor type")
        
        self.io = I_CAN(address)
        self.motor_type = motor_type
        self.control = Control(self.motor_type, self.io)
        self.telemetry = Telemetry(self.motor_type, self.io)
        self.logs = MotorLogs()

    def setup(self):
        return self.io.setup()

    def init(self):
        if self.motor_type == MotorType.RMD8x_pro:
            message = [0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            return self.io.send_cmd(message, 0.01)

        print(f"Motor of type {self.motor_type.name} initialized at address {self.io.identifier}")

    def restart(self):
        return self.init()

    def wait(self, seconds):
        time.sleep(seconds)
