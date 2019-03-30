import paho.mqtt.client as mqtt
import os, sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

COMPONENT = 'mqtt'

client = mqtt.Client()
client.connect("localhost", 1883, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

client.on_connect = on_connect
client.on_publish = on_publish                          #assign function to callback

def mqtt_publish(topic, value):
    client.publish(topic,value)    


