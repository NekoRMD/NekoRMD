# NekoRMD python

**NekoRMD** is a Python library for controlling RMD series motors through a CAN interface. It provides a wide range of functions for motor control and monitoring.

![logo.JPG](__asset__%2Flogo.JPG)
~ logo was generated using DALLE 3 ~

## TODO

- [x] Position control
- [x] Speed control
- [ ] New initialization algorithm (HIGH)
- [ ] Torque control
- [x] Full telemetry getters support
- [ ] Write tests
- [ ] Translate the documentation into English and Ru
- [ ] Finish writing the remaining commands from the official documentation
- [x] Publish in pip
- [ ] Many motors support (up to 3) using CAN
- [ ] Many motors support (up to N) using multiple serial CAN devices with command sync
- [ ] Visualization and Web control the motor

## Installation

```bash
pip install NekoRMD
```

Configure CAN in your device:
https://python-can.readthedocs.io/en/stable/installation.html


## API

Each function checks the motor CAN address to ensure it corresponds to the motor being controlled, as well as verifies the command code to confirm that the response was received for the specific command that the function is expecting.

### NekoRMD

The basic class for controlling RMD motors through a class object. When initializing in the constructor, it is mandatory to specify the CAN device address parameters and the motor type.

```python
from NekoRMD.MotorType import MotorType
from NekoRMD.NekoRMD import NekoRMD

motor = NekoRMD(address=0x149, motor_type=MotorType.RMD8x_pro)
```

`motor.setup()` - Initializes communication with the motor. Establishes a CAN connection with the motor and allows communication with it.

`motor.init()` - Sends the command to turn on the motor.

Attention! After initializing the motor, it may not respond for 10 seconds! With a high degree of probability, your problems of non-fulfillment of motor commands are solved using time.sleep(10).

Therefore, by default, the motor does not execute the following commands until 10 seconds after initialization. To disable this, execute:

```python
motor.WAIT_AFTER_INIT = False
```

`motor.restart()` - Restart the motor.

`motor.wait(secunds=5)` - # Delay task execution for a specific motor without blocking other motors and receiving data.


### Control

`motor.control.stop()` - Send a command to stop the motor.

`motor.contol.freeze()` - Send a command to freeze the motor (the motor will hold its position).

`motor.contol.unfreeze()` - Send a command to unfreeze the motor.

#### Speed control

`motor.control.speed.set_speed(degrees_per_sec)` - Send a command to control the motor speed. Sending an argument of 0 will stop the motor.

#### Position control

`set_increment_position(self, max_speed, angle)` - Control the incremental position (multi-turn mode).

**Parameters:**
- `max_speed` (int): Maximum speed in RPM.
- `angle` (int): Incremental angle in hundredths of a degree.

**Example:**
```python
motor.control.position.set_increment_position(max_speed=1000, angle=3600)
```

`set_single_turn_position(self, direction, max_speed, angle)` - Control the position within a single turn.

**Parameters:**
- `direction` (int): Rotation direction (0x00 - clockwise, 0x01 - counterclockwise).
- `max_speed` (int): Maximum speed in RPM.
- `angle` (int): Control angle in hundredths of a degree.

**Пример:**
```python
motor.control.position.set_single_turn_position(0x01, 1000, 3800)
```

`set_absolute_position(self, max_speed, angle)` - Control the absolute position (multi-turn mode).

**Examples:**
- `max_speed` (int): Maximum speed in RPM.
- `angle` (int): Absolute angle in hundredths of a degree.

**Example:**
```python
motor.control.position.set_absolute_position(max_speed=1000, angle=7200)
```

Get the current motor position. Returns `timestamp, current_position`:
```python
motor.control.position.get_position_data()
```

Output motor position to the console and logs:
```python
motor.control.position.print_position_data(is_loop=True, subscriber="gRPC-monitor")
```

#### Torque control

Send a torque control command with 1 A:
```python
motor.control.Torque.set_current(current = 1.0) # A
```


### Telemetry

> Reading acceleration value:

```python
motor.telemetry.read_acceleration()
```

> Reading software version:

```python
motor.telemetry.read_software_version()
```

return: Software version date.

> Reading motor temperature and current torque:

```python
motor.telemetry.read_motor_temperature_and_torque()
```

return: Dictionary with temperature `Temp`, torque `Iq`, speed `Speed`, and angle `Angle`.

> Reading system error status:

```python
motor.telemetry.read_system_errors()
```

return: Dictionary with system errors, brake, voltage, and temperature.

> Reading motor power:

```python
motor.telemetry.read_motor_power()
```


#### Encoder

The RMD 8X Pro motor uses two encoders:

*Relative encoder*: used to determine the current position within one revolution.

```python
motor.telemetry.print_relative_encoder()
```

Returns: (encoder_position, encoder_raw_position, encoder_offset)

It is also possible to log and print the encoder values using the method `print_relative_encoder(is_loop=False, delay=1)`.

*Absolute encoder*: used to track the motor position over several revolutions.

```python
motor.telemetry.get_absolute_encoder()
```

It is also possible to log and print the encoder values using the method `print_absolute_encoder(is_loop=False, delay=1)`.

#### PID

> Getting the value of the motor's PID parameters:

```python
motor.telemetry.read_pid_params()
```

This function sends a command to get the current PID parameters of the motor and returns them as a dictionary. The parameters include the proportional (KP) and integral (KI) coefficients for the current loop, speed loop, and position loop.

```
Returns:
    dict: Dictionary with PID parameters in the format:
        {
            "current_kp": int,
            "current_ki": int,
            "speed_kp": int,
            "speed_ki": int,
            "position_kp": int,
            "position_ki": int
        }
        If the response is incorrect, None is returned.
```

> Print motor PID parameters with repetition option:

```python
motor.telemetry.print_pid_params()
```

This function calls __print_pid_params to print the current PID parameters of the motor. 

If the is_loop parameter is set to True, the function will repeatedly print the parameters with the specified delay.

Args:
- is_loop (bool): Flag indicating whether to repeat the parameter printout. Default is False.

- delay (int): Delay between repeated parameter printouts in seconds. Default is 1 second.

> Writing PID parameters to motor RAM:

This function sends a command to write the PID parameters to the motor's random access memory (RAM).

```
Args:
    current_kp (float): Proportional coefficient for the current loop.
    current_ki (float): Integral coefficient for the current loop.
    speed_kp (float): Proportional coefficient for the speed loop.
    speed_ki (float): Integral coefficient for the speed loop.
    position_kp (float): Proportional coefficient for the position loop.
    position_ki (float): Integral coefficient for the position loop.
```

```
Returns:
    response: Device response. If the response is incorrect, None is returned.
```

> Writing PID parameters to motor ROM:

This function sends a command to write the PID parameters to the motor's read-only memory (ROM).

```
Args:
    current_kp (float): Proportional coefficient for the current loop.
    current_ki (float): Integral coefficient for the current loop.
    speed_kp (float): Proportional coefficient for the speed loop.
    speed_ki (float): Integral coefficient for the speed loop.
    position_kp (float): Proportional coefficient for the position loop.
    position_ki (float): Integral coefficient for the position loop.
```

```
Returns:
    response: Device response. If the response is incorrect, None is returned.
```


### Logs

STATUS: working on it...

> Command description:

The 8 byte CAN command can be converted into a textual description in EN-en and RU-ru languages by calling the methods of the `logs` class:

```python
motor.logs.decode_motor_message(command)
```

> Response description:

Similarly, for processing and converting motor responses into text format, you can use:

```python
motor.logs.decode_motor_response(response)
```