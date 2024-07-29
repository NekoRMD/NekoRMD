# NekoRMD python

## TODO

- [ ] translate the documentation into English

- [ ] finish writing the remaining commands from the official documentation

## Installation

```bash
pip install neko-rmd
```

Configure CAN in your device:
https://python-can.readthedocs.io/en/stable/installation.html


## API

### NekoRMD

Базовый класс управления моторами RMD через объект класса. При инициализации в конструкторе обязательно требуется указать параметры адресса CAN устройства и тип мотора.


```python
from NekoRMD.MotorType import MotorType
from NekoRMD.NekoRMD import NekoRMD

motor = NekoRMD(address=0x149, motor_type=MotorType.RMD8x_pro)
```

`motor.setup()` - Инициализация общения с мотором. Устанавливает CAN соединение с мотором и позволяет общаться с ним?

`motor.init()` - Отправка команды включения мотора.

`motor.restart()` - Перезагрузить мотор.

`motor.wait(secunds=5)` - Задержка выполнения задач для конкретного мтора без блокировки других моторов и получения данных.


### Control

`motor.control.stop()` - Отправка команды остановки мотора.

`motor.contol.freeze()` - Отправка команды заморозить мотор (мотор будет удерживать свою позицию).

#### Speed control



#### Position control

Установить позицию мотора по радианам:

```python
motor.control.position.set_position_radians(1.75)
```

Установить позицию мотора по градусам:

```python
motor.control.position.set_position_degrees(60)
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
