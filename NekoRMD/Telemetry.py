from NekoRMD.MotorType import MotorType
import time
import struct

class Telemetry:
    def __init__(self, motor_type, io, motor_address):
        if not isinstance(motor_type, MotorType):
            raise ValueError("Invalid motor type")
        
        self.motor_type = motor_type
        self.io = io
        self.motor_address = motor_address

    # ==================================================
    # |
    # |                      Telemetry
    # |
    # ==================================================

    def read_acceleration(self):
        """
        Чтение значения ускорения.

        :return: Значение ускорения.
        """
        message = [0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.1)
        if response.arbitration_id == self.motor_address and response.data[0] == 0x42:
            acceleration = struct.unpack('<H', response.data[2:4])[0]
            return acceleration
        return None
    
    def read_software_version(self):
        """
        Чтение версии программного обеспечения.

        :return: Дата версии ПО.
        """
        message = [0xB2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.1)
        if response.arbitration_id == self.motor_address and response.data[0] == 0xB2:
            version_date = struct.unpack('<H', response.data[4:6])[0]
            return version_date
        return None
    
    def read_motor_temperature_and_torque(self):
        """
        Чтение температуры мотора и текущего крутящего момента.

        :return: Словарь с температурой, крутящим моментом, скоростью и углом.
        """
        message = [0xA2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.1)
        if response.arbitration_id == self.motor_address and response.data[0] == 0xA2:
            temp, iq, speed, angle = struct.unpack('<BHHH', response.data[1:])
            return {'Temp': temp, 'Iq': iq, 'Speed': speed, 'Angle': angle}
        return None
    
    def read_system_errors(self):
        """
        Чтение состояния ошибки системы.

        :return: Словарь с ошибками системы, тормозом, напряжением и температурой.
        """
        message = [0x9A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.1)
        if response.arbitration_id == self.motor_address and response.data[0] == 0x9A:
            if len(response.data) < 4:
                raise ValueError("Received data is too short for motor power.")
            power = struct.unpack('<H', response.data[2:4])[0]
            return power
        return None

    def read_motor_power(self):
        """
        Чтение мощности мотора.

        :return: Значение мощности.
        """
        message = [0x71, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.1)
        if response.arbitration_id == self.motor_address and response.data[0] == 0x71:
            power = struct.unpack('<H', response.data[2:4])[0]
            return power
        return None


    # ==================================================
    # |
    # |                       Encoder
    # |
    # ==================================================


    # TODO: не корректно производится подсчет encoder_position
    def get_absolute_encoder(self):
        if (self.motor_type == MotorType.RMD8x_pro):
            message = [0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.01)

        # RESPONSE.DATA:
        #   
        # [0x60, 0x00, ENCODER_POS_1, ENCODER_POS_2, ENCODER_POS_3, ENCODER_POS_4, 0x00, 0x00]
        #
        # Байт 0: Код команды (0x60)
        # Байт 1: Статус ошибки (Error Status)
        # Байт 2-3: Момент текущего крутящего момента (Current Torque) (2 байта)
        # Байт 4-5: Скорость мотора (Motor Speed) (2 байта)
        # Байт 6-7: Текущая позиция (Current Position) (2 байта)

        print("Request: " + str([hex(byte) for byte in response.data]))  

        if response.arbitration_id == self.motor_address and response.data[0] == 0x60:
            encoder_position = (response.data[4] | (response.data[5] << 8) | (response.data[6] << 16) | (response.data[7] << 24))
            return encoder_position
        else:
            print("Invalid response")
        
    
    def __print_absolute_encoder(self):
        print(f"Multi-turn Encoder Position: {self.get_absolute_encoder()}")
    
    def print_absolute_encoder(self, is_loop=False, delay=1):
        self.__print_absolute_encoder()
        if is_loop:
            while True:
                self.__print_absolute_encoder()
                time.sleep(delay)
                print("=" * 30)

    def get_relative_encoder(self):
        if (self.motor_type == MotorType.RMD8x_pro):
            message = [0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.01)

        # RESPONSE.DATA
        #
        # [0x90, 0x00, ENCODER_LOW, ENCODER_HIGH, ENCODER_RAW_LOW, ENCODER_RAW_HIGH, ENCODER_OFFSET_LOW, ENCODER_OFFSET_HIGH]
        #
        # ENCODER_LOW и ENCODER_HIGH - младший и старший байты текущего положения энкодера, 
        # ENCODER_RAW_LOW и ENCODER_RAW_HIGH - младший и старший байты исходного положения энкодера, 
        # ENCODER_OFFSET_LOW и ENCODER_OFFSET_HIGH - младший и старший байты смещения нуля энкодера.

        if response.arbitration_id == self.motor_address and response.data[0] == 0x90:
            encoder_position = response.data[2] | (response.data[3] << 8)
            encoder_raw_position = response.data[4] | (response.data[5] << 8)
            encoder_offset = response.data[6] | (response.data[7] << 8)
            return encoder_position, encoder_raw_position, encoder_offset
        else:
            print("Invalid response")

    def __print_relative_encoder(self):
        encoder_position, encoder_raw_position, encoder_offset = self.get_relative_encoder()

        print(f"Encoder Position: {encoder_position}")
        print(f"Encoder Raw Position: {encoder_raw_position}")
        print(f"Encoder Offset: {encoder_offset}")
    
    def print_relative_encoder(self, is_loop=False, delay=1):
        self.__print_relative_encoder()
        if is_loop:
            while True:
                self.__print_relative_encoder()
                time.sleep(delay)
                print("=" * 30)



    # ==================================================
    # |
    # |                       PID
    # |
    # ==================================================
    
    def read_pid_params(self):
        """
        Читает PID параметры мотора.

        Эта функция отправляет команду для получения текущих PID параметров мотора и 
        возвращает их в виде словаря. Параметры включают коэффициенты пропорционального (KP) и 
        интегрального (KI) регулирования для текущего контура, контура скорости и контура позиции.

        Returns:
            dict: Словарь с PID параметрами в формате:
                {
                    "current_kp": int,
                    "current_ki": int,
                    "speed_kp": int,
                    "speed_ki": int,
                    "position_kp": int,
                    "position_ki": int
                }
                Если ответ некорректен, возвращается None.
        """

        message = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        response = self.io.send_cmd(message, 0.1)

        if response.arbitration_id == self.motor_address and response.data[0] == 0x30:
            _, _, current_kp, current_ki, speed_kp, speed_ki, position_kp, position_ki = struct.unpack("<BBBBBBBB", response.data)
            
            return {
                "current_kp": current_kp,
                "current_ki": current_ki,
                "speed_kp": speed_kp,
                "speed_ki": speed_ki,
                "position_kp": position_kp,
                "position_ki": position_ki
            }
        else:
            print("Error: Invalid response")
            return None
        
    def __print_pid_params(self):
        pid_params = self.read_pid_params()
        if pid_params:
            print(f"Current PID params:")
            print(f"  Текущий контур: KP = {pid_params['current_kp']}, KI = {pid_params['current_ki']}")
            print(f"  Контур скорости: KP = {pid_params['speed_kp']}, KI = {pid_params['speed_ki']}")
            print(f"  Контур позиции: KP = {pid_params['position_kp']}, KI = {pid_params['position_ki']}")

    def print_pid_params(self, is_loop=False, delay=1):
        """
        Выводит PID параметры мотора с возможностью повторения.

        Эта функция вызывает __print_pid_params для вывода текущих PID параметров мотора. 
        Если параметр is_loop установлен в True, функция будет повторять вывод параметров с заданной задержкой.

        Args:
            is_loop (bool): Флаг, указывающий, следует ли повторять вывод параметров. По умолчанию False.
            delay (int): Задержка между повторениями вывода параметров в секундах. По умолчанию 1 секунда.
        """
        self.__print_pid_params()
        if is_loop:
            while True:
                self.__print_pid_params()
                time.sleep(delay)
                print("=" * 30)
    
    def __convert_to_8bit(self, value, scale=1.0):
        """
        Конвертирует значение с плавающей запятой в 8-битное целое.

        Эта функция принимает значение с плавающей запятой, умножает его на заданный масштаб и 
        возвращает результат как 8-битное целое число.

        Args:
            value (float): Значение для конвертации.
            scale (float): Масштабный коэффициент. По умолчанию 1.0.

        Returns:
            int: 8-битное целое число.
        """
        return int(value * scale) & 0xFF
    
    def write_pid_params_ram(self, current_kp, current_ki, speed_kp, speed_ki, position_kp, position_ki):
        """
        Записывает PID параметры в RAM мотора.

        Эта функция отправляет команду для записи PID параметров в оперативную память (RAM) мотора.

        Args:
            current_kp (float): Коэффициент пропорционального регулирования текущего контура.
            current_ki (float): Коэффициент интегрального регулирования текущего контура.
            speed_kp (float): Коэффициент пропорционального регулирования контура скорости.
            speed_ki (float): Коэффициент интегрального регулирования контура скорости.
            position_kp (float): Коэффициент пропорционального регулирования контура позиции.
            position_ki (float): Коэффициент интегрального регулирования контура позиции.

        Returns:
            response: Ответ устройства. Если ответ некорректен, возвращается None.
        """
        message = [
            0x31, 0x00,
            self.convert_to_8bit(current_kp),
            self.convert_to_8bit(current_ki),
            self.convert_to_8bit(speed_kp),
            self.convert_to_8bit(speed_ki),
            self.convert_to_8bit(position_kp),
            self.convert_to_8bit(position_ki)
        ]
        
        response = self.io.send_cmd(message, 0.1)
        if response.arbitration_id == self.motor_address and response.data[0] == 0x31:
            return response
        else:
            print("Error: Invalid response!")
            return None
    
    def write_pid_params_rom(self, current_kp, current_ki, speed_kp, speed_ki, position_kp, position_ki):
        """
        Записывает PID параметры в ROM мотора.

        Эта функция отправляет команду для записи PID параметров в постоянную память (ROM) мотора.

        Args:
            current_kp (float): Коэффициент пропорционального регулирования текущего контура.
            current_ki (float): Коэффициент интегрального регулирования текущего контура.
            speed_kp (float): Коэффициент пропорционального регулирования контура скорости.
            speed_ki (float): Коэффициент интегрального регулирования контура скорости.
            position_kp (float): Коэффициент пропорционального регулирования контура позиции.
            position_ki (float): Коэффициент интегрального регулирования контура позиции.

        Returns:
            response: Ответ устройства. Если ответ некорректен, возвращается None.
        """
        message = [
            0x32, 0x00,
            self.convert_to_8bit(current_kp),
            self.convert_to_8bit(current_ki),
            self.convert_to_8bit(speed_kp),
            self.convert_to_8bit(speed_ki),
            self.convert_to_8bit(position_kp),
            self.convert_to_8bit(position_ki)
        ]

        response = self.io.send_cmd(message, 0.1)
        if response.arbitration_id == self.motor_address and response.data[0] == 0x32:
            return response
        else:
            print("Error: Invalid response!")
            return None
