import paho.mqtt.client as mqtt
import logging
import time


class MQTT:
    __recived_message = None
    __order_in_progress = "no"

    def __init__(self ,address, port, name) -> None:
        self.address = address
        self.port = port
        self.client = mqtt.Client(name)
        self._set_on_configs()

    def connect(self):
        logging.info(f"Connecting to Broker {self.address}.")
        self.client.connect(self.address)

    def loop_start(self):
        self.client.loop_start()

    def _set_on_configs(self):
        self.client.on_connect = MQTT.on_connect
        self.client.on_disconnect = MQTT.on_disconnect
        self.client.on_message = MQTT.on_message
        self.client.on_publish = MQTT.on_publish

    def update_order_status(self):
        self.subscribe("inventory/order_in_progress")
        time.sleep(0.5)
        self.__order_in_progress = self.__recived_message

    def publish(self, topic, msg):
        temp = self.client.publish(topic, str(msg))
        temp.wait_for_publish()

    def subscribe(self, topic):
        return self.client.subscribe(topic)

    @staticmethod
    def on_publish(mqttc, obj, mid):
        print("mid: " + str(mid))

    @staticmethod
    def on_log(client, userdata, level, buf):
        print("log: ",buf)

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connection is Ok.")
        else:
            print("Bad connection and Returned code is", rc)

    @staticmethod
    def on_disconnect(client, userdata, flags, rc=0):
        print("Disconnected and Resualt code is", rc)

    @staticmethod
    def on_message(client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode('utf-8'))
        MQTT.__recived_message = m_decode
        print(f"Recived message: {m_decode}")


class MQTTPublisher(MQTT):
    pass


class MQTTSubscriber(MQTT):
    pass
