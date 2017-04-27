import wiringpi

# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 480  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

io_initialized = False
def io_init():
    global io_initialized
    if io_initialized:
        return

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pinMode(21, wiringpi.GPIO.PWM_OUTPUT)

    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    wiringpi.pwmSetRange(MAX_SPEED)
    wiringpi.pwmSetClock(2)

    wiringpi.pinMode(20, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(25, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(26, wiringpi.GPIO.OUTPUT)

    # defaults based on page 17 of 
    # https://www.pololu.com/file/download/MC33926.pdf?file_id=0J233
    wiringpi.pinMode(12, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(16, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(23, wiringpi.GPIO.OUTPUT)
    wiringpi.pinMode(24, wiringpi.GPIO.OUTPUT)
    wiringpi.digitalWrite(12, 0) # M2D1
    wiringpi.digitalWrite(16, 1) # M2nD2
    wiringpi.digitalWrite(23, 0) # M1D1
    wiringpi.digitalWrite(24, 1) # M1nD2

    io_initialized = True

class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 0
        else:
            dir_value = 1

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        io_init()
        wiringpi.digitalWrite(self.dir_pin, dir_value)
        wiringpi.pwmWrite(self.pwm_pin, speed)

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
        wiringpi.digitalWrite(self.enable_pin, 1)

    def disable(self):
        io_init()
        wiringpi.digitalWrite(self.enable_pin, 0)

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

motors = Motors()