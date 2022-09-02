from inevntory import Inventory
from constnts import EnumColor


test = Inventory(10, 10)
test.set_xy_grid(1, 1, EnumColor.RED)
print(test.get_xy_grid_color(1, 1))