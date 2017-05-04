import time
from readRotary import Encoder
import logging
import threading
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

leftEncoder = Encoder(1, 2, "leftEncoder")

def test():
	logging.debug('Starting Left Encoder Thread')
	leftEncoder.testWhile()
	logging.debug('Ending Thread')

encoderThreadLeft = threading.Thread(name='leftEncodersThread', target=test)

encoderThreadLeft.start()

while True:
	sleep(2)
	leftEncoder.reset = True
	print "reset"
	sleep(2)
