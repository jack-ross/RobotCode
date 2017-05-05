from time import sleep
from encoders.readRotary import Encoder
from multiprocessing import Queue, Process, Value, Array
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

encoderAL = 19
encoderBL = 13

encoderCountLeft = Value('i', 0)

e = Encoder(encoderAL,encoderBL,"test")
#print "\nPINNSSSADFASDFASDF   " + str(e.encoderA)
e.initPins()

resetEncoder = Queue()



def readLeftEncoder(resetQ, count):
    logging.debug('Starting Left Encoder Process')
    encoderProcessLeft = Process(name="leftEncoder",
                                     target=e.readRotors,
                                     args=(encoderCountLeft, resetEncoder, ))
    encoderProcessLeft.start()

readLeftEncoder(encoderCountLeft, resetEncoder)


while True:        
	for i in xrange(5):
		sleep(1)
		logging.debug(encoderCountLeft)
	print "reset"
	resetEncoder.put(True)
	logging.debug(encoderCountLeft)

