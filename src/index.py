import logging
import threading
#from multiprocessing import Pool
import time

import mockMotors as mock

#Imports from other classes
#import readRotary as encoderControl
#from motors.dual_mc33926_rpi import motors, MAX_SPEED
#from MQTT.MQTTController import MQTTClient

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

#Has to be a dict b/c they are mutable
encoderCount = {"leftEncoder":0, "rightEncoder":0}
standard_speed = 50
robot_name = "Robo 1"
robot_topic_name = "robot-1"

mqttClient = MQTTClient(robot_name, robot_topic_name)

'''
----------------------Intialize Componentes----------------------------
'''
def init_Motors():
    motors.enable()
    time.sleep(2)
    motors.setSpeeds(50, 50)

def init_Encoders():
    encoderControl.initPins(19,13)

def init_Sonar():
    GPIO.setup(sonarPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def init_MQTT():
    mqttClient.run_MQtt()

def init_Robot():
    init_Motors()
    init_Encoders()
    init_Sonar()
    init_Mqtt()

'''
----------------------Thread Methods----------------------------
'''    
def readEncoder(s, count):
    logging.debug('Starting Encoder Thread')
    #Update the encoder dictionary constantly
    #encoderControl.readRotors(encoderCount)
    logging.debug(encoderCount)

def motorControl(s, eCount):
    logging.debug('Starting Motor Thread')
    logging.debug('Starting')
    #PID control
    #time.sleep(2)
    #motors.setSpeeds(0,0)
    mock.incrementLeft(eCount)
    mock.incrementRight(eCount)
    logging.debug('Exiting')

def mqttControl():
    logging.debug('Starting mqtt Thread')
    logging.debug('Starting')
    #MQTT Polling
    logging.debug('Exiting')

encoderThread = threading.Thread(name='encodersThread', target=readEncoder, args=(encoderCount,))
motorThread = threading.Thread(name='motorsThread', target=motorControl, args=(encoderCount,))
mqttThread = threading.Thread(name='mqttThread', target=mqttControl)

'''
----------------------Robot Control Methods----------------------------
''' 


#Return true if there is an object in the way
def detectObject():
    if(GPIO.input(sonarPin) == 1):
        return True
    return False

def move():
    totalTicks = 0;
    ticksToMove = mqttClient.distanceToGoal * TI_PER_CM;
    motors.setSpeeds(standard_speed, standard_speed)

    while (totalTicks < ticksToMove):
        #angle threshold
        if(abs(mqttClient.angleToGoal) > 30):
            break;

        while(detectObject() == True or mqttClient.permissionToMove == False):
            motors.setSpeeds(0,0)
        
        #Pid stuff
        extra_ticks = abs(1.2*mqttClient.angleToGoal) * TICKS_PER_DEG_TURN; // normally no multiplier on the angle
        turn_velocity = (extra_ticks + SPEED_TICKS) / SPEED_TICKS * standard_speed;

        ''' Why did we have this?
        if (abs(ticksRcheck - ticksLcheck) == (int)EXTRA_TICKS) {
        angleToGoal = 0;
        ticksRcheck = 0;
        ticksLcheck = 0;
        }'''

        if(mqttClient.angleToGoal > 0.5):
            #Steer left
            motors.setSpeeds(standard_speed, turn_velocity)
            #logging.debug("Motor speeds: ")
        elif(mqttClient.angleToGoal < 0.5):
            #Steer right
            motors.setSpeeds(turn_velocity, standard_speed)
        else:
            #go straight
            motors.setSpeeds(standard_speed, standard_speed)

        totalTicks = encoderCount['leftEncoder']

def turn(degrees):
    logging.debug("Ticks to turn: " + str(degrees))
    motors.setSpeeds(0,0)
    #maybe delay?
    #sleep(0.05)
    ticksToTurn = abs(degrees) * TICKS_PER_DEG_TURN;

    if(degrees > 0):
        motors.setSpeeds(standard_speed, -1*standard_speed)
    else:
        motors.setSpeeds(standard_speed, -1*standard_speed)

    leftDone = False
    rightDone = False;

    while (!leftDone || !rightDone):
        if(encoderCount['leftEncoder'] > ticksToTurn):
            motors.motor1.setSpeed(0)
            leftDone = True
        if(encoderCount['rightEncoder'] > ticksToTurn):
            motors.motor2.setSpeed(0)
            rightDone = True

'''
--------------------------Main----------------------------
''' 

#will this need locks? Don't this so
#Encoders writes to the dict. 
#MQTT writes to its own info
#This thread just reads their info...

'''TODO:
-Confirm Wheel calculation stuff (can put that in the encoders lib)
  -pid
'''

if __name__ == "__main__":
    encoderThread.start()
    motorThread.start()
    mqttThread.start()

    while True:
        #if the distance to goal is > 5 cm we will wait for the next goal
        if(abs(mqttClient.angleToGoal) > 30):
            turn(mqttClient.angleToGoal); 
            #we want some time for the system to send us more data
            #sleep(.1)
        
        else if(mqttClient.distanceToGoal > 5)
            move();
 






