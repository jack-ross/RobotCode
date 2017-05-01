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

#Has to be a dict b/c they are mutable
encoderCount = {"leftEncoder":0, "rightEncoder":0}

def init_Motors():
    motors.enable()
    time.sleep(2)
    motors.setSpeeds(50, 50)

def init_Encoders():
    encoderControl.initPins(19,13)

def readEncoder(count):
    logging.debug('Starting Encoder Thread')
    #Update the encoder dictionary constantly
    encoderControl.readRotors(encoderCount)
    logging.debug(encoderCount)

def motorControl():
    logging.debug('Starting Motor Thread')
    logging.debug('Starting')
    #PID control
    time.sleep(2)
    motors.setSpeeds(0,0)
    logging.debug('Exiting')

def mqttControl():
    logging.debug('Starting mqtt Thread')
    logging.debug('Starting')
    #MQTT Polling
    logging.debug('Exiting')

def init_Robot():
    init_Motors()
    init_Encoders()
    #init_Mqtt()

encoderThread = threading.Thread(name='encodersThread', target=readEncoder, args=(encoderCount))
motorThread = threading.Thread(name='motorsThread', target=motorControl)
#mqttThread = threading.Thread(name='mqttThread', target=mqttControl)

#encoderThread.start()
#motorThread.start()

#will this need locks? Encoders writes and the other one reads?
#
while True:
	print encoderCount
	time.sleep(2)