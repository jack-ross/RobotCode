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
        self.resetEncoder = Queue()
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

    def reset(self):
        self.resetEncoder.put(True)

    ''' 
    DEPRECATED?
    '''
    # count dict will hold the count for the encoder
    def readRotors(self, count, resetQ):
        try:
            while True:
                encLA_last = -1
                while resetQ.empty():
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
                if not resetQ.empty():
                    resetQ.get()
                    count = 0

        finally:
            GPIO.cleanup() # this seems wrong...?

class Encoders(object):

    def __init__(self):
        self.encoderCountLeft = Value('i', 0)
        self.encoderCountRight = Value('i', 0)

        self.leftEncoder = Encoder(encoderLeftPinA, encoderLeftPinB, "leftEncoder")
        self.rightEncoder = Encoder(encoderRightPinA, encoderRightPinB, "rightEncoder")
        
        self.leftEncoderReset = Queue()
        self.rightEncoderReset = Queue()

        self.start()

    def start(self):
        logging.debug("starting encoders")
        encoderProcessLeft = Process(name="leftEncoder",
                                     target=self.leftEncoder.readRotors,
                                     args=(self.encoderCountLeft, self.leftEncoderReset, ))
        encoderProcessRight = Process(name="rightEncoder",
                                      target=self.rightEncoder.readRotors,
                                      args=(self.encoderCountRight, self.rightEncoderReset, ))

        encoderProcessRight.start()
        encoderProcessLeft.start()

    def reset(self):
        self.leftEncoderReset.put(True)
        self.leftEncoderReset.put(True)
        
    def rightValue(self):
        return self.encoderCountRight.value
    
    def leftValue(self):
        return self.encoderCountLeft.value


encoders = Encoders()