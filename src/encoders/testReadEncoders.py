from encoders.readRotary import Endcoder

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

encoderAL = 19
encoderBL = 13

encoderCountLeft = Value('i', 0)

e = Endcoder(encoderAL,encoderBL)
resetEncoder = Queue()



def readLeftEncoder(resetQ, count):
    logging.debug('Starting Left Encoder Process')
	encoderProcessLeft = Process(name="leftEncoder",
                                     target=e.readRotors,
                                     args=(encoderCountLeft, resetEncoder, ))

while True:        
	for i in xrange(10):
		sleep(1)
		logging.debug(encoderCountLeft)

	resetEncoder.put(True)
	logging.debug(encoderCountLeft)

