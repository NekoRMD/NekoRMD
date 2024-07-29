import matplotlib.pyplot as plt
import matplotlib.animation as animation
from NekoRMD.MotorType import MotorType
from NekoRMD.NekoRMD import NekoRMD

# Инициализация двигателя
motor = NekoRMD(address=0x149, motor_type=MotorType.RMD8x_pro)
motor.setup()


fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-', animated=True)

def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(-40000, 40000)
    return ln,

def update(frame):
    timestamp, current_position = motor.control.position.get_position_data()
    xdata.append(timestamp)
    ydata.append(current_position)
    
    if len(xdata) > 100:
        xdata.pop(0)
        ydata.pop(0)
    
    ax.set_xlim(xdata[0], xdata[-1])
    
    # Автоматическое обновление границ оси y
    min_y = min(ydata) - 5000
    max_y = max(ydata) + 5000
    ax.set_ylim(min_y, max_y)
    
    ln.set_data(xdata, ydata)
    return ln,

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=100)  # Обновление каждые 0.1 секунды

plt.show()
