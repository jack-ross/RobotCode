
import logging
# import threading
import time
from multiprocessing import Queue, Process, Value

#import mockMotors as mock

#Imports from other classes
from encoders.readRotary import Encoder
from encoders import wheelConstants
from motors.dual_mc33926_rpi import motors, MAX_SPEED
from MQTT.MQTTController import MQTTClient

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

#Has to be a dict b/c they are mutable
encoderCountLeft = Value('i', 0)
encoderCountRight = Value('i', 0)
reset = Queue()

#TODO: Get proper pins
encoderRightPinA = -1
encoderRightPinB = -1
encoderLeftPinA = -1
encoderLeftPinB = -1

leftEncoder = Encoder(encoderLeftPinA, encoderLeftPinB, "leftEncoder")
rightEncoder = Encoder(encoderRightPinA, encoderRighttPinB, "rightEncoder")


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
    leftEncoder.initPins()
    rightEncoder.initPins()

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
# Need to test this
def readLeftEncoder(resetQ, count):
    logging.debug('Starting Left Encoder Process')
    #Update the encoder dictionary constantly
    global reset 

    while True:
        encLA_last = -1
        while reset.empty():    
            #logging.debug('incrementing')
            #leftEncoder.testWhile(count)
            encLA_state = GPIO.input(leftEncoder.encoderA)
            # test and uncomment this
            # encLB_state = GPIO.input(dt)
            if encLA_state != encLA_last:
                encLB_state = GPIO.input(leftEncoder.encoderB)
                if encLB_state != encLA_state:
                    count.value += 1
                else:
                    count.value += 1
                    # print count["encoderA"]
                encLA_last = encLA_state
                # sleep(0.0001)
        print count
        #remove the reset val from the queue
        reset.get()
        encoderCountLeft.value = 0

    #leftEncoder.readRotors(reset, encoderCountLeft)
    # logging.debug(encoderCountLeft)

#This is the old version
def readRightEncoder(resetQ, count):
    logging.debug('Starting Right Encoder Process')
    #Update the encoder dictionary constantly
    rightEncoder.readRotors(reset, encoderCountRight)
    # logging.debug(encoderCountRight)

def motorControl(s, eCount):
    logging.debug('Starting Motor Thread')
    logging.debug('Starting')
    #PID control
    #time.sleep(2)
    motors.setSpeeds(0,0)
    logging.debug('Exiting')

def mqttControl():
    logging.debug('Starting mqtt Thread')
    logging.debug('Starting')
    #MQTT Polling
    mqttClient.run_MQtt()
    logging.debug('Exiting')

# encoderThreadLeft = threading.Thread(name='leftEncodersThread', target=readLeftEncoder, args=(encoderCountLeft,))
# encoderThreadRight = threading.Thread(name='rightEncodersThread', target=readRightEncoder, args=(encoderCountRight,))
motorThread = threading.Thread(name='motorsThread', target=motorControl)
mqttThread = threading.Thread(name='mqttThread', target=mqttControl)

encoderProcessLeft = Process(name="leftEncoder", target=readLeftEncoder, args=(reset,count,))
encoderProcessRight = Process(name="rightEncoder", target=readRightEncoder, args=(reset,count,))


'''
----------------------Robot Control Methods----------------------------
''' 

#Sonar
#Return true if there is an object in the way
def detectObject():
    if(GPIO.input(sonarPin) == 1):
        return True
    return False

def move():
    totalTicks = 0;

    #reset the encoder counters
    global reset 
    reset.put(True)

    ticksToMove = mqttClient.distanceToGoal * TI_PER_CM;
    motors.setSpeeds(standard_speed, standard_speed)

    while (totalTicks < ticksToMove):
        #angle threshold
        if(abs(mqttClient.angleToGoal) > 30):
            break;

        while(detectObject() == True or mqttClient.permissionToMove == False):
            motors.setSpeeds(0,0)
        
        #Pid stuff
        # normally no multiplier on the angle, we added it for some reason?
        extra_ticks = abs(1.2*mqttClient.angleToGoal) * TICKS_PER_DEG_TURN; 
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

        totalTicks = encoderCountLeft.value

def turn(degrees):
    logging.debug("Ticks to turn: " + str(degrees))
    motors.setSpeeds(0,0)

    #reset the encoder counters
    global reset 
    reset.put(True)

    #maybe delay?
    #sleep(0.05)
    ticksToTurnLeft = abs(degrees) * TICKS_PER_DEG_TURN + encoderCountLeft['leftEncoder'];
    ticksToTurnRight = abs(degrees) * TICKS_PER_DEG_TURN + encoderCountLeft['rightEncoder'];

    if(degrees > 0):
        motors.setSpeeds(standard_speed, -1*standard_speed)
    else:
        motors.setSpeeds(-1*standard_speed, standard_speed)

    leftDone = False
    rightDone = False;

    while (leftDone == False or rightDone == False):
        if(encoderCountLeft.value >= ticksToTurnLeft):
            motors.motor1.setSpeed(0)
            leftDone = True
        if(encoderCountRight.value >= ticksToTurnRight):
            motors.motor2.setSpeed(0)
            rightDone = True

'''
--------------------------Main----------------------------
''' 

#will this need locks? Don't this so
#Encoders writes to the dict
#MQTT writes to its own info
#This thread just reads their info

'''TODO:
-Confirm Wheel calculation stuff (can put that in the encoders lib)
  -pid
'''

if __name__ == "__main__":
    encoderProcessLeft.start()
    encoderProcessRight.start()
    motorThread.start()
    mqttThread.start()

    mqttClient.distanceToGoal = 10

    while True:
        ''' 
        This is the code for full operation
        
        #if the distance to goal is > 5 cm we will wait for the next goal
        if(abs(mqttClient.angleToGoal) > 30):
            turn(mqttClient.angleToGoal); 
            #we want some time for the system to send us more data
            #sleep(.1)
        
        else if(mqttClient.distanceToGoal > 5)
            move();
        '''
        '''
        This is preliminary test code
        '''
        #move()
        #turn(90)
        turn(180)
        sleep(2)






