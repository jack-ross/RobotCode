import RPi.GPIO as GPIO
import time # to use delays use time.sleep(0.25)

# refer to https://learn.sparkfun.com/tutorials/raspberry-gpio
# for board layout.
# Using BCM (Broadcom Chip) Pin marking

# BCM prevents us from addressing Pins we can't use
GPIO.setmode(GPIO.BCM)

#M1IN2
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)

# M1D1
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)

# NOTM1D2
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.HIGH)

#Enable
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.HIGH)

# PWM pin up with a frequency of 1kHz, 
# and set that output to a 50% duty cycle.
pwm = GPIO.PWM(18, 1000)
pwm.start(50)

