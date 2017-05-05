from __future__ import print_function
import time
from dual_mc33926_rpi import motors, MAX_SPEED

try:
    motors.enable()
    motors.setSpeeds(100, 100)

    print("Both motors from full speed back to full speed forward")
    for dc in range(-100, 101, 5):
        motors.setSpeeds(dc,dc)
        time.sleep(0.5)

finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)
  motors.disable()
