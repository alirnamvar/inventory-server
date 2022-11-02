import paho.mqtt.client as mqtt
import time
import logging


class MQTT:
    __recived_message = None
    __order_in_progress = "no"

    def __init__(self ,address, port) -> None:
        self.address = address
        self.port = port
        self.client = mqtt.Client()
        self.__set_on_configs()
        self.connect_and_loop_start()

    def connect_and_loop_start(self):
        self.client.connect(self.address)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def get_recived_message(self):
        return self.__recived_message

    def set_recived_message_None(self):
        self.__recived_message = None

    def get_order_in_progress(self):
        return self.__order_in_progress

    def __set_on_configs(self):
        # self.client.on_connect = MQTT.on_connect
        # self.client.on_disconnect = MQTT.on_disconnect
        self.client.on_message = MQTT.on_message
        # self.client.on_publish = MQTT.on_publish

    def update_order_status(self):
        self.subscribe("inventory/order_in_progress")
        time.sleep(0.5)
        self.__order_in_progress = self.__recived_message

    def publish(self, topic, msg):
        infot = self.client.publish(topic, str(msg))
        infot.wait_for_publish()
        return infot

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
        MQTT.__has_new_order = True
        print(f"Recived message: {m_decode}")


class MQTTSubscribePLC(MQTT):

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.client = mqtt.Client()
        self.client.pallet_position = None
        self.client.has_pallet_position = False
        self.client.on_message = MQTTSubscriber.on_message

    def subscribe(self, topic):
        return self.client.subscribe(topic)

    def reset_pallet_position(self):
        self.__set_pallet_position_None()
        self.__set_has_pallet_position_false()

    def loop_stop_and_disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def set_has_pallet_position_true(self):
        self.client.has_pallet_position = True

    def get_has_pallet_position(self):
        return self.client.has_pallet_position

    def get_pallet_position(self) -> int:
        return int(self.client.pallet_position)

    def __set_pallet_position_None(self):
        self.client.pallet_position = None

    def __set_has_pallet_position_false(self):
        self.client.has_pallet_position = False

    @staticmethod
    def on_message(client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode('utf-8'))
        client.pallet_position = m_decode
        client.has_pallet_position = True
        logging.info(f"Recived pallet position is \"{m_decode}\"")