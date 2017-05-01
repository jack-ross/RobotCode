import logging
import threading
import time
import test

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

#Has to be a dict b/c they are mutable
count = {"leftEncoder":0, "rightEncoder":0}

def readEncoder(count):
    logging.debug('Starting Encoder Thread')
    initPins(19,13)
    readRotors(encoderCount)
    logging.debug(test.changeTup(count))
    #time.sleep(2)
    #logging.debug('Exiting')

def motorControl():
    logging.debug('Starting')
    time.sleep(3)
    logging.debug('Exiting')

t = threading.Thread(name='encoders', target=readEncoder, args=(count,))
# w = threading.Thread(name='motors', target=motorControl)
#w2 = threading.Thread(target=worker) # use default name

# w.start()
# w2.start()
t.start()

while True:
	print count
	time.sleep(2)