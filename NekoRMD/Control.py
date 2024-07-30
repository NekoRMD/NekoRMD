from NekoRMD.MotorType import MotorType
import struct
import time
from datetime import datetime

class Control:
    def __init__(self, motor_type, io):
        if not isinstance(motor_type, MotorType):
            raise ValueError("Invalid motor type")
        self.motor_type = motor_type
        self.io = io

        self.position = self.Position(self, self.io)
        self.speed = self.Speed(self, self.io)
        self.Torque = self.Torque(self, self.io)

    def freeze(self):
        message = [0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        return self.io.send_cmd(message, 0.01)
    
    def unfreeze(self):
        msg = [0x77, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        return self.io.send_cmd(msg, 0.01)

    class Position:
        def __init__(self, control, io):
            self.control = control
            self.io = io

        def __get_motor_position(self):
            msg = [0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            response = self.io.send_cmd(msg, delay=0.01)
            timestamp = response.timestamp
            data = response.data
            return timestamp, data

        def __parse_position_data(self, data):
            """
            Конвертирует данные ответа с двигателя в понятный формат
            :param data: список байт данных
            :return: текущая позиция энкодера, исходная позиция энкодера, нулевое смещение энкодера
            """
            current_position = data[2] << 8 | data[1]
            original_position = data[4] << 8 | data[3]
            zero_offset = data[6] << 8 | data[5]
            return current_position, original_position, zero_offset

        def get_position_data(self):
            timestamp, data = self.__get_motor_position()
            current_position, _, _ = self.__parse_position_data(data)
            return timestamp, current_position
        
        def __print_position_data(self):
            timestamp, data = self.__get_motor_position()
            current_position, original_position, zero_offset = self.__parse_position_data(data)
            
            timestamp_time = datetime.fromtimestamp(timestamp)
            current_time = datetime.now()
            time_difference = current_time - timestamp_time

            print("Current time:", current_time)
            print(f"Timestamp: {timestamp}")
            print("Delta time:", time_difference)
            print(f"Current Position: {current_position}")
            print(f"Original Position: {original_position}")
            print(f"Zero Offset: {zero_offset}")
            print("-" * 30)

        def print_position_data(self, is_loop=False):
            self.__print_position_data()
            if is_loop:
                while True:
                    self.__print_position_data()
                    now = datetime.now()

                    detailed_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                    print("Текущее время с микросекундами:", detailed_time)
                    time.sleep(0.2)


        def set_increment_position(self, max_speed, angle):
            """
            Управление приращением позиции (многооборотный режим).

            Параметры:
            ----------
            max_speed : int
                Максимальная скорость в RPM.
            angle : int
                Приращение угла в сотых долях градуса.

            Пример:
            -------
            motor.control.position.set_increment_position(max_speed=1000, angle=3600)
            """
                
            msg = [0xA8, 0x00, max_speed & 0xFF, (max_speed >> 8) & 0xFF, angle & 0xFF, (angle >> 8) & 0xFF, (angle >> 16) & 0xFF, (angle >> 24) & 0xFF]
            self.io.send_cmd(msg, 0.1)

        def set_single_turn_position(self, direction, max_speed, angle):
            """
            Управление положением на одном обороте.

            Параметры:
            ----------
            direction : int
                Направление вращения (0x00 - по часовой стрелке, 0x01 - против часовой стрелки).
            max_speed : int
                Максимальная скорость в RPM.
            angle : int
                Угол управления в сотых долях градуса.

            Пример:
            -------
            motor.control.position.set_single_turn_position(0x01, 1000, 3800)
            """
            msg = [0xA6, direction, max_speed & 0xFF, (max_speed >> 8) & 0xFF, angle & 0xFF, (angle >> 8) & 0xFF, 0x00, 0x00]
            self.io.send_cmd(msg, 0.1)

        def set_absolute_position(self, max_speed, angle):
            """
            Управление абсолютной позицией (многооборотный режим).

            Параметры:
            ----------
            max_speed : int
                Максимальная скорость в RPM.
            angle : int
                Абсолютный угол в сотых долях градуса.

            Пример:
            -------
            motor.control.position.set_absolute_position(max_speed=1000, angle=7200)
            """
                
            msg = [0xA4, 0x00, max_speed & 0xFF, (max_speed >> 8) & 0xFF, angle & 0xFF, (angle >> 8) & 0xFF, (angle >> 16) & 0xFF, (angle >> 24) & 0xFF]
            self.io.send_cmd(msg, 0.1)


    class Speed:
        def __init__(self, control, io):
            self.control = control
            self.io = io
        
        def set_speed(self, speed=0):
            """
            Sends a speed control command to the motor via the CAN bus.

            This function forms and sends command 0xA2 to control the speed of the motor output shaft.
            The speed value is transmitted in the int32_t format and corresponds to a speed of 0.01 degrees/second per least significant bit (LSB).

            Parameters:
            - speed (float): The desired speed in degrees per second. The value can be positive or negative to control the direction of rotation.

            Notes:
            - The speed value will be rounded to the nearest integer.
            - A speed of 0 will stop the motor.
            - Check the range of allowable speeds for your motor in the technical documentation.

            Example usage:
            motor.control.speed.set_speed(100)
            """
            speedControl = int(speed / 0.01)
            msg = [0xA2, 0x00, 0x00, 0x00, 
                speedControl & 0xFF, 
                (speedControl >> 8) & 0xFF, 
                (speedControl >> 16) & 0xFF, 
                (speedControl >> 24) & 0xFF]
            # print("Request: " + str([hex(byte) for byte in msg]))   
            return self.io.send_cmd(msg, 0.1)

    class Torque:
        def __init__(self, control, io):
            self.control = control
            self.io = io
        
        def test(self):
            message = [0xA1, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00]
            return self.io.send_cmd(message, 0.01)

        def __calculate_crc(self, data):
            crc = 0xFFFF
            for pos in data:
                crc ^= pos
                for _ in range(8):
                    if (crc & 1) != 0:
                        crc >>= 1
                        crc ^= 0xA001
                    else:
                        crc >>= 1
            return crc
        
        def set_current(self, current):
            command = 0xA1
            current_mA = int(current * 100)

            message = [
                command,
                0x00, # NULL
                current_mA & 0xFF, # Torque Current Low Byte
                (current_mA >> 8) & 0xFF, # Torque Current High Byte
                0x00, # NULL
                0x00, # NULL
                0x00, # NULL
                0x00  # NULL
            ]

            # Calculate CRC
            crc = self.__calculate_crc(message)
            message.append(crc & 0xFF) # CRC Low Byte
            message.append((crc >> 8) & 0xFF) # CRC High Byte

            # Ensure the message is exactly 8 bytes for CAN
            if len(message) > 8:
                message = message[:8]
            elif len(message) < 8:
                message += [0x00] * (8 - len(message))

            print([hex(num) for num in message])  # Print hex values for debugging

            response = self.io.send_cmd(message, 0.01)
            return response