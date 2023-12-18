"""
Rotate the motor with the specified velocity to reach the target position.

Author: ASU

"""

import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1111
import time

pytrinamic.show_info()

connectionManager = ConnectionManager()  # If no Interface is selected , the default interface is usb_tmcl
with connectionManager.connect() as myInterface: 
    module = TMCM1111(myInterface)
    motor = module.motors[0]

    # Please be sure not to use a too high current setting for your motor.

    print("Preparing parameters")
    # preparing drive settings
    motor.drive_settings.max_current = 128
    motor.drive_settings.standby_current = 0
    motor.drive_settings.boost_current = 0
    motor.drive_settings.microstep_resolution = motor.ENUM.microstep_resolution_256_microsteps
    print(motor.drive_settings)

    # preparing linear ramp settings
    motor.max_acceleration = 51200
    motor.max_velocity = 51200

    # reset actual position
    motor.actual_position = 0

    # start rotating motor in different directions
    print("Rotating...")
    motor.rotate(51200)
    time.sleep(5)

    # stop rotating motors
    print("Stopping...")
    motor.stop()

    # read actual position
    print("ActualPostion = {}".format(motor.actual_position))
    time.sleep(2)

    # short delay and move back to start
    print("Moving back to 0")
    motor.move_to(0)

    # wait until position 0 is reached
    while not(motor.get_position_reached()):
        print("target position motor: " + str(motor.target_position) + " actual position motor: " + str(motor.actual_position))
        time.sleep(0.2)

    print("Reached Position 0")

print("\nReady.")