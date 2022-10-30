from constants import EnumColor


class Finder:
    list_of_coordinates = []
    coordinates_bank = []

    def initiate(self, iut_inventory, red: int, green: int, blue: int, white: int) -> None:
        self.inventory = iut_inventory
        self.red = red
        self.green = green
        self.blue = blue
        self.white = white

    def is_coordinate_in_list(self, x: int, y: int) -> bool:
        for coordinate in self.list_of_coordinates:
            if coordinate[0] == x and coordinate[1] == y:
                return True
        return False

    def find_selected_color(self, enum_color: EnumColor) -> tuple:
        for x in range(self.inventory.x):
            for y in range(self.inventory.y):
                if self.inventory.get_xy_grid_color(x, y) == enum_color.name:
                    if self.is_coordinate_in_list(x, y):
                        continue
                    return (x, y)
        return None

    def main_finder(self) -> list:
        while self.red > 0 or self.green > 0 or self.blue > 0 or self.white > 0:
            if self.red > 0:
                self.list_of_coordinates.append(
                    self.find_selected_color(EnumColor.RED))
                self.red -= 1
            if self.green > 0:
                self.list_of_coordinates.append(
                    self.find_selected_color(EnumColor.GREEN))
                self.green -= 1
            if self.blue > 0:
                self.list_of_coordinates.append(
                    self.find_selected_color(EnumColor.BLUE))
                self.blue -= 1
            if self.white > 0:
                self.list_of_coordinates.append(
                    self.find_selected_color(EnumColor.WHITE))
                self.white -= 1
        return self.list_of_coordinates

    def clear_material_coordinate_list(self) -> None:
        self.coordinates_bank.append(self.list_of_coordinates)
        self.list_of_coordinates = []

    def update_coordinates(self, coordinates: list) -> None:
        for coordinate in coordinates:
            self.inventory.empty_coordinate(coordinate[0], coordinate[1])