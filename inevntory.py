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
        logging.info('Arranging inventory raw materials...')
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
        self.print_inventory()

    def update_inventory(self, red, green, blue, white, redis_server) -> None:
        red_in_server, green_in_server, \
            blue_in_server, white_in_server = self._get_materials_from_server(redis_server)

        redis_server.set('red', red_in_server - red)
        redis_server.set('green', green_in_server - green)
        redis_server.set('blue', blue_in_server - blue)
        redis_server.set('white', white_in_server - white)
        logging.info("Inventory has updated.")
        self.print_inventory()

    def _get_materials_from_server(self, redis_server) -> tuple:
        _red = int(redis_server.get('red').decode('utf-8'))
        _green = int(redis_server.get('green').decode('utf-8'))
        _blue = int(redis_server.get('blue').decode('utf-8'))
        _white = int(redis_server.get('white').decode('utf-8'))
        return (_red, _green, _blue, _white)

    @staticmethod
    def make_mobile_order(colors_part : str, material_coordinate_list : list) -> str:
        colors_part += "#"
        position = "#".join(["".join(map(str, i)) for i in material_coordinate_list])
        return colors_part + position

    def _set_grid_houses(self, color: int, position: str) -> None:
        _x = int(position[0])
        _y = int(position[1])
        if color == EnumColor.RED.value:
            self.set_xy_grid(x=_x, y=_y, color=EnumColor.RED)
        elif color == EnumColor.GREEN.value:
            self.set_xy_grid(x=_x, y=_y, color=EnumColor.GREEN)
        elif color == EnumColor.BLUE.value:
            self.set_xy_grid(x=_x, y=_y, color=EnumColor.BLUE)
        elif color == EnumColor.WHITE.value:
            self.set_xy_grid(x=_x, y=_y, color=EnumColor.WHITE)

    def update(self, materials_position : str, redis_server):
        parts = materials_position.split('#')
        colors = parts.pop(0)
        server_colors = self._get_materials_from_server(redis_server)

        if len(colors) == 4:
            redis_server.set_colors(
                red=server_colors[0] + int(colors[0]),
                green=server_colors[1] + int(colors[1]),
                blue=server_colors[2] + int(colors[2]),
                white=server_colors[3] + int(colors[3]),
            )
            color_value = 0
            for color in colors:
                color_value += 1
                for i in range(int(color)):
                    position = parts.pop(0)
                    self._set_grid_houses(color_value, position)

        elif len(colors) == 3:
            redis_server.set_colors(
                red=server_colors[0],
                green=server_colors[1] + int(colors[0]),
                blue=server_colors[2] + int(colors[1]),
                white=server_colors[3] + int(colors[2]),
            )
            color_value = 1
            for color in colors:
                color_value += 1
                for i in range(int(color)):
                    position = parts.pop(0)
                    self._set_grid_houses(color_value, position)

        elif len(colors) == 2:
            redis_server.set_colors(
                red=server_colors[0],
                green=server_colors[1],
                blue=server_colors[2] + int(colors[0]),
                white=server_colors[3] + int(colors[1]),
            )
            color_value = 2
            for color in colors:
                color_value += 1
                for i in range(int(color)):
                    position = parts.pop(0)
                    self._set_grid_houses(color_value, position)

        elif len(colors) == 1:
            redis_server.set_colors(
                red=server_colors[0],
                green=server_colors[1],
                blue=server_colors[2],
                white=server_colors[3] + int(colors[0]),
            )
            color_value = 4
            for i in range(int(colors[0])):
                position = parts.pop(0)
                self._set_grid_houses(color_value, position)
        self.print_inventory()

    def place_selected_materials(self, number: int, enum_color: EnumColor) -> None:
        for i in range(1, number + 1):
            coor = tuple(input(f'Place {enum_color.name}{i} in: '))
            coor = [i for i in coor if i.isnumeric()]
            self.set_xy_grid(x=int(coor[0]), y=int(coor[1]), color=enum_color)

    def print_inventory(self) -> None:
        print('Inventory Status:\n', self.__grid, '\n')

    def set_xy_grid(self, *,  x: int, y: int, color: EnumColor) -> None:
        self.__grid[x][y] = color.value

    def get_xy_grid_color(self, x: int, y: int) -> EnumColor:
        return EnumColor(self.__grid[x][y]).name

    def empty_coordinate(self, x: int, y: int) -> None:
        self.__grid[x][y] = 0
