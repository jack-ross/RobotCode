
import logging
import time
from multiprocessing import Queue, Process, Value
from encoders.readRotary import encoders
from encoders import wheelConstants
from motors.dual_mc33926_rpi import motors, MAX_SPEED
from MQTT.MQTTController import MQTTClient
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

# CONSTANTS
ONE_REV = 3592/4 # encoder ticks
WHEEL_CIRCUM = 25.1327 # centimeters
TI_PER_CM = ONE_REV / WHEEL_CIRCUM
TICKS_PER_DEG_REV = ONE_REV / 360
ROBOT_WIDTH = 22.8
DEG_PER_REV = WHEEL_CIRCUM * 360 / 2 / 3.14159 / ROBOT_WIDTH
TICKS_PER_DEG_TURN = ONE_REV / DEG_PER_REV
SPEED_TICKS = 2124

#Has to be a dict b/c they are mutable
encoderCountLeft = Value('i', 0)
encoderCountRight = Value('i', 0)
reset = Queue()

#TODO: Get proper pins
encoderRightPinA = -1
encoderRightPinB = -1
encoderLeftPinA = -1
encoderLeftPinB = -1
sonarPin = 12

# MQTT Variables
distanceToGoal = 0
angleToGoal = 0
permissionToMove = True

standard_speed = 50
robot_name = "Robo 1"
robot_topic_name = "robot-1"

mqttClient = MQTTClient(robot_name, robot_topic_name, distanceToGoal, angleToGoal, permissionToMove)


'''
----------------------Intialize Componentes----------------------------
'''

def init_Encoders():
    encoders.start()

def init_Sonar():
    GPIO.setup(sonarPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def init_MQTT():
    logging.debug('Starting mqtt Thread')
    logging.debug('Starting')
    mqttClient.run_Mqtt()

def init_Motors():
    motors.enable()
    motors.setSpeeds(0,0)

def init_Robot():
    init_Motors()
    init_Encoders()
    # init_Sonar()
    init_MQTT()

'''
----------------------Thread Methods----------------------------
'''    

def mqttControl():
    #MQTT Polling
    mqttClient.run_Mqtt()

mqttThread = Process(name='mqttThread', target=mqttControl)


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
    logging.debug("moving")
    totalTicks = 0
    encoders.reset()
    time.sleep(0.25)
    
    ticksToMove = distanceToGoal * TI_PER_CM
    motors.setSpeeds(standard_speed, standard_speed)

    while (totalTicks < ticksToMove):
        #angle threshold
        if(abs(angleToGoal) > 30):
            logging.debug("angle greater than zero")    
            break

        while(detectObject() == True or permissionToMove == False):
            logging.debug("blocked")            
            motors.setSpeeds(0,0)
        
        # adjust speed of one side if robot is getting off track
        extra_ticks = abs(1.2*angleToGoal) * TICKS_PER_DEG_TURN; 
        turn_velocity = (extra_ticks + SPEED_TICKS) / SPEED_TICKS * standard_speed

        if(angleToGoal > 0.5): #Steer left
            logging.debug("steer left")
            motors.setSpeeds(standard_speed, turn_velocity)
        elif(angleToGoal < -0.5): #Steer right
            logging.debug("steer right")
            motors.setSpeeds(turn_velocity, standard_speed)
        else: #go straight
            logging.debug("move straight")
            motors.setSpeeds(99, 99)

        totalTicks = encoders.leftValue()

def turn(degrees):
    logging.debug("Ticks to turn: " + str(degrees))
    motors.setSpeeds(0,0)

    #reset the encoder counters
    encoders.reset()

    logging.debug("encoder val left " + str(encoders.leftValue()))
    logging.debug("encoder val right " + str(encoders.rightValue()))

    #maybe delay?
    time.sleep(0.25)
    ticksToTurnLeft = abs(degrees) * TICKS_PER_DEG_TURN + encoders.leftValue() - 100
    ticksToTurnRight = abs(degrees) * TICKS_PER_DEG_TURN + encoders.rightValue() - 100

    logging.debug("Ticks to turn left " + str(ticksToTurnLeft))
    logging.debug("Ticks to turn right " + str(ticksToTurnRight))

    if(degrees > 0):
        motors.setSpeeds(standard_speed, -1*standard_speed)
    else:
        motors.setSpeeds(-1*standard_speed, standard_speed)

    leftDone = False
    rightDone = False

    while leftDone == False or rightDone == False:
        if encoders.leftValue() >= ticksToTurnLeft:
            motors.motor1.setSpeed(0)
            leftDone = True
        if encoders.rightValue() >= ticksToTurnRight:
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

    # init_Robot()
    mqttThread.start()
    motors.enable()
    distanceToGoal = 10
    # motors.setSpeeds(0, 0)
    
    try:
        while True:
            
            # #if the distance to goal is > 5 cm we will wait for the next goal
            # if(abs(angleToGoal) > 30):
            #     logging.debug("turning")
            #     turn(angleToGoal); 
            #     #we want some time for the system to send us more data
            #     #sleep(.1)
            
            # elif distanceToGoal > 5:
            #     logging.debug("moving1")
                
            #     move()

            '''
            This is preliminary test code
            '''
            #move()
            turn(90)
            
            #motors.setSpeeds(50, 50)
            time.sleep(2)
            turn(180)
            #motors.setSpeeds(0, 0)
            time.sleep(2)
            turn(270)
            time.sleep(2)
            turn(360)
            time.sleep(2)
            
    finally:
        GPIO.cleanup()





