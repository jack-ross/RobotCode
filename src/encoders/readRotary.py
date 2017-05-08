from RPi import GPIO
import logging
import threading 
import time
from multiprocessing import Queue, Process, Value, Array

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


#note these values worked for left encoder
encoderAL = 19
encoderBL = 13
encLA_last = -1
count = 0

# TODO: Get proper pins
encoderRightPinA = 4
encoderRightPinB = 17 # not used
encoderLeftPinA = 19
encoderLeftPinB = 13 # not used

class Encoder(object):
    def __init__(self, encoderAPin, encoderBPin, name):
        self.encoderName = name
        self.encoderA = encoderAPin
        self.encoderB = encoderBPin # not used
        self.lock = threading.Lock()
        self.resetEncoder = Queue()
        self.initPins()

    def initPins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.encoderA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.encoderB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
        encLA_last = -1
	try:
            while True:

                while resetQ.empty():
                    #logging.debug("Counting")
                    encLA_state = GPIO.input(self.encoderA)
                    # test and uncomment this
                    # encLB_state = GPIO.input(dt)
                    if encLA_state != encLA_last:
                        count.value += 1
                            # print count["encoderA"
			logging.debug(str(self.encoderName) + "tick num: " + str(count.value))
                        encLA_last = encLA_state
                if not resetQ.empty():
                    logging.debug("reseting")
                    resetQ.get()
                    count.value = 0

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
        self.rightEncoderReset.put(True)
        
    def rightValue(self):
        return self.encoderCountRight.value
    
    def leftValue(self):
        return self.encoderCountLeft.value


encoders = Encoders()

