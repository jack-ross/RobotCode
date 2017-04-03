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

#Enable
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.HIGH)

##### Motor 1

# M1IN1
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.HIGH)

#M1IN2
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

# M1D1
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)

# NOTM1D2
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.HIGH)

##### Motor 2

#M2D1
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)

#M2barD2
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.HIGH)

# M2IN1
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)

# M2IN2
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)


# PWM pin up with a frequency of 1kHz,
# and set that output to a 50% duty cycle.
pwm = GPIO.PWM(18, 500)
pwm.start(90)
time.sleep(2.5)
GPIO.cleanup()  
