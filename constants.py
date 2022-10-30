from enum import Enum
import os


WAITING_TIME_IN_SECONDS = 2
INVENTORY_X = 4
INVENTORY_Y = 4

clear_screen = lambda: os.system('cls' if os.name=='nt' else 'clear')

class EnumColor(Enum):
    EMPTY = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    WHITE = 4
