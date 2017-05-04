#from RPi import GPIO
import threading 
#note these values worked for left encoder
encoderAL = 19
encoderBL = 13
encLA_last = -1
count = 0

# TODO: Add init for other encoder and pins

class Encoder(object):
    def __init__(self, encoderAPin, encoderBPin, name):
        self.encoderName = name
        self.encoderA = encoderAPin
        self.encoderB = encoderBPin
        #self.lock = threading.Lock()
        self.reset = False

    def initPins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.encoderA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.encoderB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        encLA_last_state = GPIO.input(self.encoderAL)

    def testWhile(self):
        while True:
            while self.reset == False:
                pass

            self.reset = False
            print "reset that guy"


    # count dict will hold the count for the encoder
    def readRotors(self, countDict):
        try:
            while True:
                encLA_last = -1
                while self.reset == False:
                    encLA_state = GPIO.input(self.encoderA)
                    # test and uncomment this
                    # encLB_state = GPIO.input(dt)
                    if encLA_state != encLA_last:
                        encLB_state = GPIO.input(self.encoderB)
                        if encLB_state != encLA_state:
                            countDict[self.encoderName] += 1
                        else:
                            countDict[self.encoderName] += 1
                            # print count["encoderA"]
                        encLA_last_state = encLA_state
                        # sleep(0.0001)

                #Will this work?
                countDict[self.encoderName] = 0
                self.reset = False
        finally:
            GPIO.cleanup()

