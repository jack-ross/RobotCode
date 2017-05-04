#Wheel info stuff
import threading
import math

#encoder ticks
ONE_REV_TICKS = 3592; 
#centimeters
WHEEL_CIRCUM = 25.1327; 
TICKS_PER_CM =  ONE_REV_TICKS / WHEEL_CIRCUM;
TICKS_PER_DEG_REV = ONE_REV_TICKS / 360;
ROBOT_WIDTH = 22.8;

# ticks to rotate the robot 1 degree
DEG_PER_REV = WHEEL_CIRCUM * 360 / 2 / math.pi / ROBOT_WIDTH; #degrees
TICKS_PER_DEG_TURN = ONE_REV_TICKS / DEG_PER_REV;


# SPEED @ 128 is 2124 ticks per half second
#SPEED_TICKS = 2124;
#consufed about this
