from encoders.readRotary import encoders
from encoders import wheelConstants
from dual_mc33926_rpi import motors
import RPi.GPIO as GPIO
from multiprocessing import Process

# CONSTANTS
ONE_REV = 3592 # encoder ticks
WHEEL_CIRCUM = 25.1327 # centimeters
TI_PER_CM = ONE_REV / WHEEL_CIRCUM
TICKS_PER_DEG_REV = ONE_REV / 360
ROBOT_WIDTH = 22.8

leftEncoder = encoders.leftEncoder
rightEncoder = encoders.rightEncoder
standard_speed = 50
sonarPin = 17
def init_Sonar():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sonarPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class MotorController(object):

    def __init__(self):
        self.totalTicks = 0
        self.ticksToMove = 0
        init_Sonar()
        motors.enable()
        motors.setSpeeds(0,0)
        encoders.start()

        self.moveAndTurnThread = Process(target=None)

    def detectObject(self):
        if(GPIO.input(sonarPin) == 1):
            return True
        return False

    def stop(self):
        if self.moveAndTurnThread.is_alive():
            self.moveAndTurnThread.terminate()

    def move(self, distance, angleToGoal):
        # check if already running move thread
        # if so, cancel it,
        #create new thread running movePrivate
        # with updated distance

        if (abs(angleToGoal) > 30): 
            # if moving
            motors.setSpeeds(0,0)
                # turn

            #if turning 
                # kill turn 
                # turn with new value
            return 
        
        # else update moving
        # if moving, kill move
        self.movePrivate(distance, angleToGoal)

    def movePrivate(self, distance, angleToGoal):

        #reset the encoder counters
        encoders.reset()

        totalTicks = 0
        ticksToMove = distance * TI_PER_CM

        while (totalTicks < ticksToMove):

            # detect blocked path from sonar
            while self.detectObject():
                motors.setSpeeds(0, 0)
            
            #Pid stuff
            # normally no multiplier on the angle, we added it for some reason?
            extra_ticks = abs(1.2*angleToGoal) * TICKS_PER_DEG_TURN; 
            turn_velocity = (extra_ticks + SPEED_TICKS) / SPEED_TICKS * standard_speed;

            # angle may be sharp
            if angleToGoal > 0.5:
                #Steer left
                motors.setSpeeds(standard_speed, turn_velocity)
                #logging.debug("Motor speeds: ")
            elif angleToGoal < 0.5:
                #Steer right
                motors.setSpeeds(turn_velocity, standard_speed)
            else:
                #go straight
                motors.setSpeeds(standard_speed, standard_speed)

            totalTicks = encoders.rightValue
            # end while loop
        
        # stop motors
        motors.setSpeeds(0, 0)
