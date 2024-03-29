import os, sys
import json
import asyncio
from helpers.db import *
# from components.mqtt.publish import mqttpublish

logger = formatLogger(__name__)
COMPONENT = "mqtt"

CONFIG_PARAMETERS = {"topic_subscribe":"text","topic_state":"text","topic_publish":"text","topic_publish_value":"text"}
ACTIONS = {"state","brightness"}


class switch(object):
    def __init__(self):
        self.topic = 0


    def dispatchNotification(self,deviceData,state):
        stateText = "Off"
        notificationClass = "default"
        if state:
            stateText = "On"
            notificationClass = "success"
        roomName = deviceData["room_name"] or "Unknown"
        deviceName = deviceData["name"] or "Unknown"
        message = deviceName + " Switch Turned <b>"+stateText+"</b>"
        dbStoreNotification(notificationClass,"device",roomName,message)
        dbPushNotification(notificationClass,"device",roomName,message)
                



    def validateProperties(self,getDevice,conditionProperties,conditionType):
        validStatus = False
        getDeviceProperties = getDevice["properties"]
        getDeviceState = getDevice["state"]
        getDevicePropertiesKeys = []
        for key, value in getDeviceProperties.items():
            getDevicePropertiesKeys.append(key)    

        for key, value in conditionProperties.items():
            if key == "state":
                if value == getDeviceState:
                    validStatus = True
            else:        
                if key in getDevicePropertiesKeys:
                    getDeviceProperty = getDeviceProperties[key]
                    getIfProperty = conditionProperties[key]
                        
                    if conditionType == "=":
                        if getDeviceProperty == getIfProperty:
                            validStatus = True

                    elif conditionType == ">":
                        if getDeviceProperty > getIfProperty:
                            validStatus = True

                    elif conditionType == "<":
                        if getDeviceProperty < getIfProperty:
                            validStatus = True
        return validStatus
        
    
    def triggerAction(self,getDevice,conditionProperties):
        triggered = False
        if "state" in conditionProperties:
            state = conditionProperties["state"]
            getParmeter = getDevice["parameters"]
            topic_publish = getParmeter["topic_publish"]
            topic_publish_topic = topic_publish["topic"]
            topic_publish_values = topic_publish["values"]
            
            importModule = __import__("components.mqtt", fromlist="*")
            importDeviceClass = getattr(importModule, "mqttPublish")
            deviceClass = importDeviceClass()
            deviceClass.publish(topic_publish_topic,topic_publish_values[int(state)])    
            

            triggered = True
        else:
            logger.error("The Device does not support this action")    
        return triggered


    def checkStateChanged(self,currentState,newState):
        state = False
        if newState != currentState:
            state = True
        return state

    def convertStateValues(self,getDevice,mqttPayload):
        getParmeter = getDevice["parameters"]
        topic_publish = getParmeter["topic_publish"]
        topic_publish_values = topic_publish["values"]
        for key, value in topic_publish_values.items():
            if value == mqttPayload:
                return key


   

    async def deviceHandler(self,topic,mqttPayload,getDevice):         
            getParmeter = getDevice["parameters"]
            getDeviceId = getDevice["id"]          
            topic_data = getParmeter["topic_data"]
            topic_state = getParmeter["topic_state"]
            deviceProperties = mqttPayload
            deviceActions = {"action":"allowed"}
            deviceAddress = None
            topic_start_part = None
            topic_key = None
            state = False 

            if topic_state:
                topic_state_find = topic_state.find('.')
                if(topic_state_find != -1):
                    topic_state_value = topic_state.split('.')
                    topic_start_part = topic_state_value[0]
                    topic_key = topic_state_value[1]
                else:
                    topic_start_part = topic_state    
            else:
                logger.error("State topic empty could not receive parse data")

            #check all incoming matching topics
            if(topic==(topic_data or topic_start_part)):
                logger.info(topic+' => '+str(mqttPayload))   
                if isinstance(mqttPayload,dict):
                    if "mac" in mqttPayload.keys():
                        deviceAddress = mqttPayload["mac"]
                    if topic_key:
                        if topic_key in deviceProperties.keys():
                            newState = int(deviceProperties[topic_key])
                            currentState = int(getDevice["state"])
                            state = self.checkStateChanged(currentState,newState)
                            
                            dbSync = dbSyncDevice(deviceAddress,COMPONENT,"switch",deviceProperties,deviceActions,newState)
                            if dbSync and state:
                                self.dispatchNotification(getDevice,newState)
                    else:
                        dbSync = dbSyncDevice(deviceAddress,COMPONENT,"switch",deviceProperties,deviceActions)
                        if dbSync and state and topic_key:
                            self.dispatchNotification(getDevice,newState)
                else:
                    newState = int(self.convertStateValues(getDevice,mqttPayload))
                    currentState = int(getDevice["state"])
                    state = self.checkStateChanged(currentState,newState)
                    dbSync = dbSyncDevice(getDevice["address"],COMPONENT,"switch",getDevice["properties"],deviceActions,newState)
                    if dbSync and state:
                        self.dispatchNotification(getDevice,newState)


            
            


            
