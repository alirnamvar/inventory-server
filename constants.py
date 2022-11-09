from enum import Enum
import os


WAITING_2_SECONDS = 2
WAITING_1_SECOND = 1
WAITING_100_MILLISECOND = 0.1
WAITING_500_MILLISECOND = 0.5
INVENTORY_X = 4
INVENTORY_Y = 4
WAREHOUSE_X = 5
WAREHOUSE_Y = 5

clear_screen = lambda: os.system('cls' if os.name=='nt' else 'clear')

WAREHOUSE_TABLE_DESCRIPTION = '''
    CREATE TABLE warehouse
    (
        position INT NOT NULL,
        red INT,
        green INT,
        blue INT,
        white INT,
        PRIMARY KEY (position)
    )
    '''
DISASSEMBLE_ORDERS_TABLE_DESCRIPTION =  '''
    CREATE TABLE disassemble_orders
    (
        disorder_number INT NOT NULL,
        position INT,
        PRIMARY KEY (order_number)
    )
    '''


class EnumColor(Enum):
    EMPTY = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    WHITE = 4
