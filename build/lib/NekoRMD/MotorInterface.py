class MotorInterface:
    def init(self):
        raise NotImplementedError

    def get_PID(self):
        raise NotImplementedError

    def set_position(self, position):
        raise NotImplementedError

    def set_speed(self, speed):
        raise NotImplementedError
