import RPi.GPIO as GPIO
import time # to use delays use time.sleep(0.25)

# ----- PI PIN OUT ----
# refer to https://learn.sparkfun.com/tutorials/raspberry-gpio
# for board layout.
# Using BCM (Broadcom Chip) Pin marking

# ----- MOTOR CONTROLER PIN OUT ----
# https://www.pololu.com/product/1213


# BCM prevents us from addressing Pins we can't use
GPIO.setmode(GPIO.BCM)
pin = 12
GPIO.setup(pin, GPIO.OUT)
try:
	while True: 
		while GPIO.input(pin) == 1:
			pass
		while GPIO.input(pin) == 0:
			pass
		start = time.time()
		while GPIO.input(pin) == 1:
			pass
		stop = time.time()
		elapsed = stop - start
		print elapsed/147/0.000001
except KeyboardInterrupt:
	print "exiting"

finally:  
    GPIO.cleanup() # this ensures a clean exit 
