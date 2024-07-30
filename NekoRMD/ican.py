import os
import time
import can


class I_CAN:
    def __init__(self, identifier):
        self.bus = None
        self.identifier = identifier
    
    def setup(self):
        try:
            os.system("sudo /sbin/ip link set can0 up type can bitrate 1000000")
            time.sleep(0.1)
        except Exception as e:
            print(e)

        try:
            bus = can.interface.Bus(bustype='socketcan', channel='can0')
            self.bus = bus
        except OSError:
            print('err: PiCAN board was not found.')
            exit()
        except Exception as e:
            print(e)

        return self.bus

    def send_cmd(self, data, delay):
        """
        Отправка команды через интерфейс CAN.

        Параметры:
        ----------
        msg : список
            Команда в формате списка байтов.
        delay : float
            Задержка перед отправкой следующей команды (по умолчанию 0.01 секунды).
        """
        
        if len(data) != 8:
            raise ValueError("Data length should be exactly 8 bytes")
        message = can.Message(arbitration_id=self.identifier,
                              data=data, is_extended_id=False)
        try:
            self.bus.send(message)
            time.sleep(delay)
            received_message = self.bus.recv()
            return received_message
        except can.CanError as e:
            print(f"Message NOT sent: {e}")