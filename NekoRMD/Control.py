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

                    # Выводим максимально подробное время
                    detailed_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
                    print("Текущее время с микросекундами:", detailed_time)
                    time.sleep(0.2)


        # Функция для установки позиции двигателя в радианах
        def set_position_radians(self, position):
            position_int = int(position * 100)  # Преобразование радианов в значение для отправки
            # Команда для установки позиции (0xA4)
            msg = [0xA4, 0x00, 0x00, 0x00, 
                (position_int & 0xFF), 
                (position_int >> 8) & 0xFF, 
                (position_int >> 16) & 0xFF, 
                (position_int >> 24) & 0xFF]
            response = self.io.send_cmd(msg, 0.01)
            
            print("sending: " + str(msg))

            # Проверка ответа
            if response.data[0] == 0xA4:
                if response.data[1:8] == [0x00, 0x00, 0x00, 0x00, 0x00, 0xF3, 0x00]:
                    raise Exception("Ошибка: двигатель не может достичь установленной позиции")
                return response
            else:
                raise Exception("Неверный ответ от двигателя")

        # Функция для установки позиции двигателя в градусах
        def set_position_degrees(self, position):
            position_radians = position * (3.141592653589793 / 180)  # Преобразование градусов в радианы
            return self.set_position_radians(position_radians)


    class Speed:
        def __init__(self, control, io):
            self.control = control
            self.io = io
        
        def set_speed(self, speed):
            pass

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