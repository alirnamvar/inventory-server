import numpy as np
from constants import WAREHOUSE_X, WAREHOUSE_Y

class Warehouse:
    __grid = None
    __pallet_numbers = 0
    __last_occupied_home = 0
    __occupied_homes = []

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.__grid = np.zeros((x, y))

    def print_warehouse(self) -> None:
        print('Warehouse Status:\n', self.__grid, '\n')

    def update(self, position: str):
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

    def remove_pallet(self, position: str):
        position = int(position)
        Warehouse.__pallet_numbers -= 1
        Warehouse.__occupied_homes.pop()
        x = position // WAREHOUSE_Y
        y = position % WAREHOUSE_X
        self.__grid[x, y] = 0
        self.print_warehouse()

    def find_pallet_position(self):
        self.__last_occupied_home += 1
        return str(self.__last_occupied_home)

    def get_pallet_number(self) -> int:
        return self.__pallet_numbers

    def get_occupied_homes(cls) -> list:
        return self.__occupied_homes