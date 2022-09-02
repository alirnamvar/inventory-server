import time
import logging
import sys

from handlers.redis_handler import RedisHandler
from handlers.order_handler import OrderHandler

# import handlers

from finder import Finder
from inevntory import Inventory
from constnts import *

# Set up logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


def main():
    # input_server = input("Server: ")
    # input_port = int(input("Port: "))
    input_server = "localhost"
    input_port = 6379
    order_number = 0
    orders_list = []
    material_coordinate_list = []

    # Create a redis server, connect to it and initiate it
    redis_server = RedisHandler(server=input_server, port=input_port)
    redis_server.flush()

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
        if order_number != redis_server.get_order_number():
            # show and update order_number
            logging.info("New order received.")
            order_number = redis_server.get_order_number()
            logging.info(f'order number: {order_number}')

            # parse and process order
            red, green, blue, white, inprogress_order = \
                order_handler.process_new_order(order_number, redis_server)
            orders_list.append(inprogress_order)

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
