import logging
from constants import EnumColor, clear_screen
import numpy as np


class Inventory:
    __grid = None

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.__grid = np.zeros((x, y))

    def arrange(self, redis_server) -> None:
        logging.info('Arranging raw materials...')
        ee = tuple(
            input("Enter each material in following format (R, G, B, W): "))
        red, green, blue, white = [i for i in ee if i.isnumeric()]
        redis_server.set('red', red)
        redis_server.set('green', green)
        redis_server.set('blue', blue)
        redis_server.set('white', white)
        logging.info("Number of materials updated in Redis server.")
        print("HINT: Enter coordinates in (x, y) format.")
        self.place_selected_materials(int(red), EnumColor.RED)
        self.place_selected_materials(int(green), EnumColor.GREEN)
        self.place_selected_materials(int(blue), EnumColor.BLUE)
        self.place_selected_materials(int(white), EnumColor.WHITE)
        clear_screen()
        logging.info("Inventory arranged.\n")

    def update_inventory(self, red, green, blue, white, redis_server) -> None:
        red_in_server = int(redis_server.get('red').decode('utf-8'))
        green_in_server = int(redis_server.get('green').decode('utf-8'))
        blue_in_server = int(redis_server.get('blue').decode('utf-8'))
        white_in_server = int(redis_server.get('white').decode('utf-8'))

        redis_server.set('red', red_in_server - red)
        redis_server.set('green', green_in_server - green)
        redis_server.set('blue', blue_in_server - blue)
        redis_server.set('white', white_in_server - white)
        logging.info("Inventory has updated.")
        self.print_grid()

    def place_selected_materials(self, number: int, enum_color: EnumColor) -> None:
        for i in range(1, number + 1):
            coor = tuple(input(f'Place {enum_color.name}{i} in: '))
            coor = [i for i in coor if i.isnumeric()]
            self.set_xy_grid(x=int(coor[0]), y=int(coor[1]), color=enum_color)

    def print_grid(self) -> None:
        print('Inventory Status:\n', self.__grid, '\n')

    def set_xy_grid(self, *,  x: int, y: int, color: EnumColor) -> None:
        self.__grid[x][y] = color.value

    def get_xy_grid_color(self, x: int, y: int) -> EnumColor:
        return EnumColor(self.__grid[x][y]).name

    def empty_coordinate(self, x: int, y: int) -> None:
        self.__grid[x][y] = 0
