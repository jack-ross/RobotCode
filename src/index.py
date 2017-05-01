import logging
import threading
#from multiprocessing import Pool
import time
import test

import readRotary as encoderControl

from motors.dual_mc33926_rpi import motors, MAX_SPEED
 
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def init_Motors():
    motors.enable()
    time.sleep(2)
    motors.setSpeeds(0, 0)

def init_Encoders():

#Has to be a dict b/c they are mutable
encoderCount = {"leftEncoder":0, "rightEncoder":0}

def readEncoder(count):
    logging.debug('Starting Encoder Thread')
    encoderControl.initPins(19,13)
    encoderControl.readRotors(encoderCount)
    logging.debug(encoderCount)

def motorControl():
    logging.debug('Starting Motor Thread')
    logging.debug('Starting')
    #PID control
    logging.debug('Exiting')

def mqttControl():
    logging.debug('Starting mqtt Thread')
    logging.debug('Starting')
    #MQTT Polling
    logging.debug('Exiting')

def 
init_Motors()

encoderThread = threading.Thread(name='encodersThread', target=readEncoder, args=(count,))
motorThread = threading.Thread(name='motorsThread', target=motorControl)
mqttThread = threading.Thread(name='mqttThread', target=mqttControl)

encoderThread.start()
motorThread.start()

#will this need locks? Encoders writes and the other one reads?
#
while True:
	print count
	time.sleep(2)