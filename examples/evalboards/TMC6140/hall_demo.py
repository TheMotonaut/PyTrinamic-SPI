"""
Move a motor back and forth using velocity and position mode of the TMC6300
"""
import time
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.evalboards import TMC6140_eval

pytrinamic.show_info()

with ConnectionManager().connect() as my_interface:
    print(my_interface)

    eval_board = TMC6140_eval(my_interface)
    motor = eval_board.motors[0]

    # configure
    motor.set_commutation_mode(1)
    motor.set_hall_order(0)

    print("Rotating...")
    motor.set_target_pwm(8000)
    time.sleep(3)

    print("Stopping...")
    motor.set_target_pwm(0)
    time.sleep(2)

    print("Rotating back...")
    motor.set_target_pwm(-8000)
    time.sleep(3)

    print("Stopping...")
    motor.set_target_pwm(0)

print("\nReady.")
