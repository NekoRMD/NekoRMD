# NekoRMD python

**NekoRMD** is a Python library for controlling RMD series motors through a CAN interface. It provides a wide range of functions for motor control and monitoring.

![logo.JPG](__asset__%2Flogo.JPG)
~ logo was generated using DALLE 3 ~

## TODO

- [x] Position control
- [x] Speed control
- [ ] New initialization algorithm (HIGH)
- [ ] Torque control
- [ ] Full telemetry getters support
- [ ] Write tests
- [ ] Translate the documentation into English and Ru
- [ ] Finish writing the remaining commands from the official documentation
- [ ] Publish in pip
- [ ] Many motors support (up to 3) using CAN

## Installation

```bash
pip install neko-rmd
```

Configure CAN in your device:
https://python-can.readthedocs.io/en/stable/installation.html


## API

### NekoRMD

The basic class for controlling RMD motors through a class object. When initializing in the constructor, it is mandatory to specify the CAN device address parameters and the motor type.

```python
from NekoRMD.MotorType import MotorType
from NekoRMD.NekoRMD import NekoRMD

motor = NekoRMD(address=0x149, motor_type=MotorType.RMD8x_pro)
```

`motor.setup()` - Initializes communication with the motor. Establishes a CAN connection with the motor and allows communication with it.

`motor.init()` - Sends the command to turn on the motor.

Attention! After initializing the motor, it may not respond for 10 seconds! With a high degree of probability, your problems of non-fulfillment of motor commands are solved using time.sleep(10)

`motor.restart()` - Перезагрузить мотор.

`motor.wait(secunds=5)` - Задержка выполнения задач для конкретного мтора без блокировки других моторов и получения данных.


### Control

`motor.control.stop()` - Отправка команды остановки мотора.

`motor.contol.freeze()` - Отправка команды заморозить мотор (мотор будет удерживать свою позицию).

`motor.contol.unfreeze()` - Отправка команды разморозить мотор.

#### Speed control

`motor.control.speed.set_speed(degrees_per_sec)` - Отправка команды управления мотором по скорости. Отправка аргумента 0 остановит мотор.

#### Position control

`set_increment_position(self, max_speed, angle)` - Управление приращением позиции (многооборотный режим).

**Параметры:**
- `max_speed` (int): Максимальная скорость в RPM.
- `angle` (int): Приращение угла в сотых долях градуса.

**Пример:**
```python
motor.control.position.set_increment_position(max_speed=1000, angle=3600)
```

`set_single_turn_position(self, direction, max_speed, angle)` - Управление положением на одном обороте.

**Параметры:**
- `direction` (int): Направление вращения (0x00 - по часовой стрелке, 0x01 - против часовой стрелки).
- `max_speed` (int): Максимальная скорость в RPM.
- `angle` (int): Угол управления в сотых долях градуса.

**Пример:**
```python
motor.control.position.set_single_turn_position(0x01, 1000, 3800)
```

`set_absolute_position(self, max_speed, angle)` - Управление абсолютной позицией (многооборотный режим).

**Параметры:**
- `max_speed` (int): Максимальная скорость в RPM.
- `angle` (int): Абсолютный угол в сотых долях градуса.

**Пример:**
```python
motor.control.position.set_absolute_position(max_speed=1000, angle=7200)
```

Получить текущую позиию мотора. Вернет `timestamp, current_position`:
```python
motor.control.position.get_position_data()
```

Вывод в консоль и логи позиции мотора:
```python
motor.control.position.print_position_data(is_loop=True, subscriber="gRPC-monitor")
```

#### Torque control

Отправка команды управления моментом при 1 А:
```python
motor.control.Torque.set_current(current = 1.0) # A
```


### Telemetry

Получение данных экодера:

```python
motor.telemetry.get_encoder()
```

Также возможно вывести в логи и консоль значения энкодера использовав метод `print_encoder()`.

Получение значения PID:

```python
motor.telemetry.get_PID()
```

Для вывода в консоль и логи используется метод `print_PID()`.


### Logs

Команду 8 byte CAN можно преобразовать в текстовое описание на EN-en и RU-ru языках вызвов методы класса `logs`:

```python
motor.logs.decode_motor_message(command)
```

Также для обработки и преобразования в текстовый формат ответов мотора можно использовать:

```python
motor.logs.decode_motor_response(response)
```
