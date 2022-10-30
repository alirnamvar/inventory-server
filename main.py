import time
import logging
import sys
import os

from handlers.redis_handler import RedisHandler
from handlers.order_handler import OrderHandler

# import handlers
from finder import Finder
from inevntory import Inventory
from mqtt import MQTT
from constants import *

# Set up logging setup
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


def main():
    # input_server = input("Server: ")
    # input_port = int(input("Port: "))
    input_redis_server = "localhost"
    input_redis_port = 6379
    broker_addres = "localhost"
    broker_port = 1883

    order_number = 0
    list_of_orders_in_tuple = []
    material_coordinate_list = []
    status = {
        'assemble_in_progress' : "no",
        'disassemble_in_progress' : False,
    }

    # Create a redis server, connect to it and initiate it
    redis_server = RedisHandler(server=input_redis_server, port=input_redis_port)
    redis_server.flush()

    mqtt_client = MQTT(broker_addres, broker_port, 'inventory')
    mqtt_client.connect()
    mqtt_client.loop_start()

    # create usable objects
    order_handler = OrderHandler()
    my_finder = Finder()

    # make inventory and arrange it
    iut_inventory = Inventory(x=INVENTORY_X, y=INVENTORY_Y)
    iut_inventory.arrange(redis_server)
    iut_inventory.print_grid()

    # Check if the connection is successful or not
    if redis_server.get_connection_status():
        logging.info("Connection to redis server established.")
        order_number = redis_server.get_order_number()
    else:
        logging.error("Connection to redis server failed.")
        exit(1)

    logging.info("Waiting for new order...")
    while redis_server.get_connection_status():
        while status['assemble_in_progress'] == "yes":
            os.system('cls' if os.name == 'nt' else 'clear') # clear screen
            logging.info("An assembly order in progress, please wait...")
            mqtt_client.update_order_status()
            status['assemble_in_progress'] = mqtt_client.__order_in_progress
            time.sleep(2)
            '''
            we subscribe to a "inventory/order_in_progress" topic and its output should be "yes" or "no".
            'mqtt_client.update_order_status()' function update 'mqtt_client.order_in_progress' to "yes" or "no".
            '''
        if order_number != redis_server.get_order_number():
            # show and update order_number
            logging.info("New order received.")
            order_number = redis_server.get_order_number()
            logging.info(f'order number: {order_number}')

            # parse and process order
            red, green, blue, white, inprogress_order = \
                order_handler.process_new_order(order_number, redis_server)
            list_of_orders_in_tuple.append(inprogress_order)

            # Serach in inventory to find materials
            my_finder.initiate(iut_inventory, red, green, blue, white)
            material_coordinate_list = my_finder.main_finder()
            logging.info(f'Material coordinate {material_coordinate_list}')

            # update coordinates and print the grid
            my_finder.update_coordinates(material_coordinate_list)
            my_finder.clear_material_coordinate_list()

            # update inventory materials
            iut_inventory.update_inventory(
                red, green, blue, white, redis_server)
            # TODO: send data to mobile robot
            order_to_mobile_robot = "".join(list_of_orders_in_tuple[order_number])
            mqtt_client.publish("inventory/order", order_to_mobile_robot)

        time.sleep(WAITING_TIME_IN_SECONDS)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        logging.warning('Interrupt happend, server terminated.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
