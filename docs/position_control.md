## Управление Положением

### `set_increment_position(self, max_speed, angle)`

Управление приращением позиции (многооборотный режим).

**Параметры:**
- `max_speed` (int): Максимальная скорость в RPM.
- `angle` (int): Приращение угла в сотых долях градуса.

**Пример:**
```python
motor.control.position.set_increment_position(max_speed=1000, angle=3600)
```

### `set_single_turn_position(self, direction, max_speed, angle)`

Управление положением на одном обороте.

**Параметры:**
- `direction` (int): Направление вращения (0x00 - по часовой стрелке, 0x01 - против часовой стрелки).
- `max_speed` (int): Максимальная скорость в RPM.
- `angle` (int): Угол управления в сотых долях градуса.

**Пример:**
```python
motor.control.position.set_single_turn_position(direction=0x01, max_speed=1000, angle=3800)
```

### `set_absolute_position(self, max_speed, angle)`

Управление абсолютной позицией (многооборотный режим).

**Параметры:**
- `max_speed` (int): Максимальная скорость в RPM.
- `angle` (int): Абсолютный угол в сотых долях градуса.

**Пример:**
```python
motor.control.position.set_absolute_position(max_speed=1000, angle=7200)
```

### `get_position_data()`

Получить текущую позицию мотора.

**Возвращает:**
- `timestamp` (float): Временная метка текущего положения.
- `current_position` (int): Текущая позиция мотора в сотых долях градуса.

**Пример:**
```python
timestamp, current_position = motor.control.position.get_position_data()
```

### `print_position_data(is_loop, subscriber)`

Вывод в консоль и логи позиции мотора.

**Параметры:**
- `is_loop` (bool): Определяет, будет ли функция работать в цикле.
- `subscriber` (str): Имя подписчика для получения данных (например, "gRPC-monitor").

**Пример:**
```python
motor.control.position.print_position_data(is_loop=True, subscriber="gRPC-monitor")
```
