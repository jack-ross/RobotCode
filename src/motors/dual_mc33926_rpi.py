import time
import RPi.GPIO as GPIO
import logging 
# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 100  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

io_initialized = False
def io_init():
    global io_initialized
    if io_initialized:
        logging.error("Global io_initialized var was true")
        return

    GPIO.setmode(GPIO.BCM)

    # PWM pins
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(18, GPIO.LOW) # M2D1
    GPIO.output(21, GPIO.LOW) # M2D1

    # direction and enables
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)

    # defaults based on page 17 of 
    # https://www.pololu.com/file/download/MC33926.pdf?file_id=0J233
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output(12, GPIO.LOW) # M2D1
    GPIO.output(16, GPIO.HIGH) # M2nD2
    GPIO.output(23, GPIO.LOW) # M1D1
    GPIO.output(24, GPIO.HIGH) # M1nD2

    io_initialized = True

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin):
        self.dir_pin = dir_pin
        self.pwm_pin = GPIO.PWM(pwm_pin, 500)  # frequency=20kHz
        self.pwm_pin.start(100)

    # speed between -100 and 100
    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 0
        else:
            dir_value = 1
            speed = 100 - speed

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        GPIO.output(self.dir_pin, dir_value)
        self.pwm_pin.ChangeDutyCycle(speed)

class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        #  pwm_pin(in2), dir_pin(in1)
        io_init()
        self.motor1 = Motor(18, 26)
        self.motor2 = Motor(21, 20)
        self.enable_pin = 25

    def enable(self):
        io_init()
        GPIO.output(self.enable_pin, 1)

    def disable(self):
        io_init()
        GPIO.output(self.enable_pin, 0)

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

motors = Motors()
