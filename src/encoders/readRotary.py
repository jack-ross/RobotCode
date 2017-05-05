from RPi import GPIO
import logging
import threading 
import time
from multiprocessing import Queue, Process, Value, Array

#note these values worked for left encoder
encoderAL = 19
encoderBL = 13
encLA_last = -1
count = 0

# TODO: Get proper pins
encoderRightPinA = -1
encoderRightPinB = -1
encoderLeftPinA = -1
encoderLeftPinB = -1

class Encoder(object):
    def __init__(self, encoderAPin, encoderBPin, name):
        self.encoderName = name
        self.encoderA = encoderAPin
        self.encoderB = encoderBPin
        self.lock = threading.Lock()
        self.reset = False
        self.initPins()

    def initPins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.encoderA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.encoderB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        encLA_last_state = GPIO.input(self.encoderA)

    def testWhile(self, count):
        time.sleep(1)
        print type(count)
        count.value = count.value +1

    ''' 
    DEPRECATED?
    '''
    # count dict will hold the count for the encoder
    def readRotors(self, reset, count):
        try:
            while True:
                encLA_last = -1
                while reset.empty():
                    encLA_state = GPIO.input(self.encoderA)
                    # test and uncomment this
                    # encLB_state = GPIO.input(dt)
                    if encLA_state != encLA_last:
                        encLB_state = GPIO.input(self.encoderB)
                        if encLB_state != encLA_state:
                            count.value += 1
                        else:
                            count.value += 1
                            # print count["encoderA"]
                        encLA_last_state = encLA_state
                        # sleep(0.0001)

        finally:
            GPIO.cleanup()

class Encoders(object):

    def __init__(self):
        self.encoderCountLeft = Value('i', 0)
        self.encoderCountRight = Value('i', 0)
        self.resetEncoders = Queue()

        self.leftEncoder = Encoder(encoderLeftPinA, encoderLeftPinB, "leftEncoder")
        self.rightEncoder = Encoder(encoderRightPinA, encoderRightPinB, "rightEncoder")

    def start(self):
        encoderProcessLeft = Process(name="leftEncoder",
                                     target=self.leftEncoder.readRotors,
                                     args=(self.reset, self.encoderCountLeft, ))
        encoderProcessRight = Process(name="rightEncoder",
                                      target=self.rightEncoder.readRotors,
                                      args=(self.reset, self.encoderCountRight, ))

        encoderProcessRight.start()
        encoderProcessLeft.start()

    def reset(self):
        self.resetEncoders.put(True)

    def rightValue(self):
        return self.encoderCountRight.value
    
    def leftValue(self):
        return self.encoderCountLeft.value


encoders = Encoders()