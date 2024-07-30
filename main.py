from NekoRMD.MotorType import MotorType
from NekoRMD.NekoRMD import NekoRMD

motor = NekoRMD(address=0x149, motor_type=MotorType.RMD8x_pro)
motor.setup()

# motor.init()
# motor.control.unfreeze()
# for i in range(10, 200, 20):
#     print(i)
#     print(str(motor.control.speed.set_speed(i)))
#     motor.wait(3)
# print("100")
# motor.control.speed.set_speed(0)
# motor.control.unfreeze()
# motor.control.speed.set_speed(100)
# print("3000")
# motor.control.speed.set_speed(3000)
# motor.control.Torque.test()
# motor.control.position.set_position_radians(0.5)
# motor.control.position.set_increment_position(1000, 3600)
motor.control.position.set_single_turn_position(0x01, 1000, 3800)
# motor.control.position.set_absolute_position(1000, 7200)
# motor.control.position.print_position_data(is_loop=True)




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
