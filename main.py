from NekoRMD.MotorType import MotorType
from NekoRMD.NekoRMD import NekoRMD

motor = NekoRMD(address=0x149, motor_type=MotorType.RMD8x_pro)
motor.setup()


motor.control.position.print_position_data(is_loop=True)




# motor.init()
# motor.wait(2)
# motor.control.Torque.test()
# motor.control.Torque.test()

# print("i: " + str(motor.control.position.get_motor_position()))

# print("o: " + str(motor.control.position.set_position_radians(1.57)))

# print(motor.control.position.get_motor_position())
# motor.wait(2)

# print(motor.control.position.set_position_degrees(90))
# print(motor.control.position.get_motor_position())
