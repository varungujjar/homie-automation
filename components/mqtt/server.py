import os, sys, json
from ast import literal_eval
import logging
import asyncio

COMPONENT = "mqtt" 
SUPPORTED_HEADERS = {"class"}
SUPPORTED_DEVICES = {"switch","light"}

from hbmqtt.client import MQTTClient, ClientException, ConnectException
from hbmqtt.mqtt.constants import QOS_1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(levelname)s %(message)s')
# logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='/tmp/myapp.log',filemode='w')


config = {
    'keep_alive': 10,
    'ping_delay': 1,
    'default_qos': 0,
    'default_retain': False,
    'auto_reconnect': True,
    'reconnect_max_interval': 5,
    'reconnect_retries': 10
}

C = MQTTClient(config=config)


def mqttPublish(topic, value):
    asyncio.ensure_future(publish(topic, value))


@asyncio.coroutine
def mqttHandler():
    yield from C.connect('mqtt://0.0.0.0:1883')
    yield from C.subscribe([('#', QOS_1)])
    logger.info("[MQTT] Subscribed to #")
    try:
        while True:
            message = yield from C.deliver_message()
            packet = message.publish_packet
            topic = packet.variable_header.topic_name
            payload = str(packet.payload.data.decode())
            mqttPayload = json.loads(payload)
            if isinstance(mqttPayload,dict):
                for key, value in mqttPayload.items():
                    if key in SUPPORTED_HEADERS:
                        logger.info(mqttPayload)
                        if value in SUPPORTED_DEVICES:
                            importDevice = __import__(value)
                            importDeviceClass = getattr(importDevice, value)
                            deviceClass = importDeviceClass()    
                            deviceClass.deviceHandler(topic,payload)    
                            try:
                                pass
                            except ImportError as error:
                                print(error)
                            except Exception as exception:
                                print(exception)
                        else:
                            print("[MQTT] Server Device Not Supported")       
                    else:
                        pass
            
        # yield from C.unsubscribe(['#'])
        # logger.info("UnSubscribed")
        # yield from C.disconnect()
    except ClientException as ce:
        logger.error("[MQTT] Client exception: %s" % ce)


@asyncio.coroutine
def publish(topic, value):
    yield from C.connect('mqtt://0.0.0.0:1883')
    tasks = [
        asyncio.ensure_future(C.publish(topic, bytes(str(value),"UTF-8"), qos=QOS_1))
    ]
    yield from asyncio.wait(tasks)
    logger.info("[MQTT] Message Published")
    yield from C.disconnect()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(mqttHandler())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
    