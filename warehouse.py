import numpy as np
from constants import WAREHOUSE_X, WAREHOUSE_Y

class Warehouse:
    __grid = None
    __pallet_numbers = 0

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.__grid = np.zeros((x, y))

    def print_warehouse(self) -> None:
        print('Warehouse Status:\n', self.__grid, '\n')

    @classmethod
    def get_pallet_number(cls):
        return cls.__pallet_numbers

    def update_pallet_position(self, position):
        if position is None:
            print("DANGER: position is None!")
            return
        Warehouse.__pallet_numbers += 1
        position = int(position)
        x = position // WAREHOUSE_Y
        y = position % WAREHOUSE_X
        self.__grid[x, y] = 1
