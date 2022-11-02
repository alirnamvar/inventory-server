import numpy as np
from constants import WAREHOUSE_X, WAREHOUSE_Y

class Warehouse:
    __grid = None
    __pallet_numbers = 0
    __occupied_homes = []

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.__grid = np.zeros((x, y))

    def print_warehouse(self) -> None:
        print('Warehouse Status:\n', self.__grid, '\n')

    def update(self, position):
        if position is None:
            print("DANGER: position is None!")
            return
        position = int(position)
        Warehouse.__pallet_numbers += 1
        Warehouse.__occupied_homes.append(position)
        x = position // WAREHOUSE_Y
        y = position % WAREHOUSE_X
        self.__grid[x, y] = 1
        self.print_warehouse()

    def get_pallet_number(self) -> int:
        return self.__pallet_numbers

    def get_occupied_homes(cls) -> list:
        return self.__occupied_homes