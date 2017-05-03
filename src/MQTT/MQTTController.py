import paho.mqtt.client as mqtt
import logging 

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

robot_name = "Robo 1"
robot_topic_name = "robot-1"
#Intialize to -1 so always reset
lastMsgRecvTime = -1

class MQTTClient(object):
	def __init__(self, robot_name, robot_topic_name):
		self.robot_name = robot_name
		self.robot_topic_name = robot_topic_name
		self.distanceToGoal = 0
		self.angleToGoal = 0
		self.permissionToMove = False
		init_Mqtt()

	def on_connect(self, client, userdata, flags, rc):
	    logging.debug("Robot 1 connected")

	def on_message(self, client, userdata, msg):
	    logging.debug(str(msg.payload))
	    '''parsed = json.loads(str(msg.payload))
	    x=parsed['x']
	    y=parsed['y']
	    curMsgRecievedTime = parsed['time']
	    if(curMsgRecievedTime > lastMsgRecvTime)
	    	logging.debug(self.robot_name + "recieved good message")
	    	lastMsgRecvTime = curMsgRecvTime
	    	self.distanceToGoal = root["distanceToGoal"];
		    self.angleToGoal = root["angleToGoal"];
		    self.permissionToMove = root["permissionToMove"];
		'''

	def init_Mqtt(self):
		#------------Init MQTT connection on local host------------
	    self.mqttc = mqtt.Client(self.robot_name)
	    ##Want to confirm this?
	    self.mqttc.connect("::1", 1883, 60)
	    self.mqttc.onconnect = self.on_connect
	    self.mqttc.on_message = self.on_message
	
	def run_Mqtt(self):
		self.mqttc.subscribe(self.robot_topic_name, 0)
	    self.mqttc.loop_forever()
	    #TODO: Change this to loop(2)

''' Old MQTT code 
	//we have recieved the msot recent msg from the server
		  if(curMsgRecvTime > lastMsgRecvTime){
		    Serial.println("New msg");
		    lastMsgRecvTime = curMsgRecvTime;
		    self.distanceToGoal = root["distanceToGoal"];
		    self.angleToGoal = root["angleToGoal"];
		    self.permissionToMove = root["permissionToMove"];
		    Serial.println(distanceToGoal);
		    totalTicks=0;
		    ticksRcheck = 0;
		    ticksLcheck = 0;
		    recievedNewMsg = true;
		  }
		  // Print values.
		  Serial.println(distanceToGoal);
		  Serial.println(angleToGoal);
		  Serial.println(curMsgRecvTime);
  '''