from RPi import GPIO

encoderAL = 19
encoderBL = 13
encLA_last_state = -1
count = 0

# TODO: Add init for other encoder and pins


def initPins(encoderALPin, encoderBLPin):
    encoderAL = encoderALPin
    encoderBL = encoderBLPin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoderAL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(encoderBL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    encLA_last_state = GPIO.input(encoderAL)

# count dict will hold the count for the encoer


def readRotors(countDict):
    try:

        while True:
            encLA_state = GPIO.input(encoderAL)
            # test and uncomment this
            # encLB_state = GPIO.input(dt)
            if encLA_state != encLA_last_state:
                encLB_state = GPIO.input(encoderBL)
                if encLB_state != encLA_state:
                    countDict["leftEncoder"] += 1
                else:
                    countDict["leftEncoder"] += 1
                    # print count["encoderA"]
                encLA_last_state = encLA_state
                # sleep(0.0001)
    finally:
        GPIO.cleanup()
