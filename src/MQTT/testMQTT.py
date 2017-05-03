import paho.mqtt.client as mqtt
from MQTTController import MQTTClient

client = MQTTClient("Robo1", "robot-1")

client.run_Mqtt()



#client.loop_forever()