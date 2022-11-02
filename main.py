import time
import logging
import sys
import os

from handlers.sql_handler import SQLHandler
from handlers.redis_handler import RedisHandler
from handlers.order_handler import OrderHandler

# import handlers
from constants import *
from finder import Finder
from warehouse import Warehouse
from inevntory import Inventory
from mqtt import MQTT, MQTTSubscribePLC, MQTTSubscribeMR


# Set up logging setup
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


def main():
    # input_server = input("Server: ")
    # input_port = int(input("Port: "))
    broker_configs = {
        "address" : "localhost",
        "port" : 1883,
    }
    redis_configs = {
        "server" : "localhost",
        "port" : 6379,
    }
    sql_configs = {
        "server" : "localhost",
        "user" : "alirnamvar",
        "database" : "IUT",
    }

    order_number = 0
    disorder_number = 0
    list_of_orders_in_tuple = []
    material_coordinate_list = []

    # Create servers, connect to and initiate it
    sql_server = SQLHandler(**sql_configs)
    redis_server = RedisHandler(**redis_configs)
    redis_server.flush()

    mqtt_client = MQTT(**broker_configs)
    mqtt_sub_plc = MQTTSubscribePLC(**broker_configs)
    mqtt_sub_mobile_robot = MQTTSubscribeMR(**broker_configs)

    # create usable objects
    order_handler = OrderHandler()
    my_finder = Finder()

    # make warehouse annd inventory then arrange it
    iut_warehouse = Warehouse(WAREHOUSE_X, WAREHOUSE_Y)
    iut_inventory = Inventory(INVENTORY_X, INVENTORY_Y)
    iut_inventory.arrange(redis_server)

    # Check if the connection is successful or not
    if redis_server.get_connection_status():
        logging.info("Connection to redis server established.")
        order_number = redis_server.get_order_number()
    else:
        logging.error("Connection to redis server failed.")
        exit(1)

    logging.info("Waiting for new order...")
    while redis_server.get_connection_status():

        # process assemble order
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
            logging.info(f'Material(s) coordinate {material_coordinate_list}')

            # update coordinates and print the grid
            my_finder.update_coordinates(material_coordinate_list)
            my_finder.clear_material_coordinate_list()

            # update inventory materials
            iut_inventory.update_inventory(red, green, blue, white, redis_server)

            # send order to mobile robot
            order_to_mobile_robot = str(list_of_orders_in_tuple[order_number - 1])
            mqtt_client.publish("inventory/order", order_to_mobile_robot)
            logging.info("Order sent to mobile robot.")

            # make mqtt client for PLC
            HAVE_PALLET_POSITION = False
            mqtt_sub_plc.connect_and_loop_start()
            mqtt_sub_plc.subscribe("warehouse/palletPosition")

            # waiting for pallet position
            while not HAVE_PALLET_POSITION:
                time.sleep(WAITING_100_MILLISECOND)
                if mqtt_sub_plc.get_has_pallet_position():
                    HAVE_PALLET_POSITION = True
                    pallet_position = mqtt_sub_plc.get_pallet_position()
                    iut_warehouse.update(pallet_position)
                    sql_server.update_warehouse((red, green, blue, white), pallet_position)
                    mqtt_sub_plc.reset_pallet_position()
            mqtt_sub_plc.loop_stop_and_disconnect()

        # process disassemble order
        elif disorder_number != redis_server.get_disorder_number():
            # show and update disorder_number
            logging.info("New Disassemble order received.")
            disorder_number = redis_server.get_disorder_number()
            logging.info(f'Disassemble order number: {disorder_number}')

            pallet_positon_to_plc = order_handler.process_new_disassemble_order(
                disorder_number, redis_server)

            # send pallet position to PLC
            mqtt_client.publish('warehouse/palletPosition', str(pallet_positon_to_plc))
            logging.info('Position of pallet sent to PLC.')

            # listen to 'materialsPosition' topic
            HAVE_MATERIALS_POSITION = False
            mqtt_sub_mobile_robot.connect_and_loop_start()
            mqtt_sub_mobile_robot.subscribe("inventory/materialsPosition")

            # waiting for materials position
            while not HAVE_MATERIALS_POSITION:
                time.sleep(WAITING_100_MILLISECOND)
                if mqtt_sub_mobile_robot.get_has_materials_position():
                    HAVE_MATERIALS_POSITION = True
                    materials_position = mqtt_sub_mobile_robot.get_materials_position()
                    iut_inventory.update(materials_position)
            mqtt_sub_mobile_robot.loop_stop_and_disconnect()

        time.sleep(WAITING_2_SECONDS)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        logging.warning('Interrupt happend, server terminated!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
