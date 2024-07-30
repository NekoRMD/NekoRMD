from NekoRMD.MotorType import MotorType

class Telemetry:
    def __init__(self, motor_type, io):
        if not isinstance(motor_type, MotorType):
            raise ValueError("Invalid motor type")
        self.motor_type = motor_type
        self.io = io

    def get_encoder(self):
        if (self.motor_type == MotorType.RMD8x_pro):
            message = [0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        return self.io.send_cmd(message, 0.01)
    
    def print_encoder(self):
        pass

    def get_PID(self):
        pass

    def print_PID(self):
        pass
        # pid_values = self.get_PID()
        # print(f"PID values: P={pid_values['P']}, I={pid_values['I']}, D={pid_values['D']}")
