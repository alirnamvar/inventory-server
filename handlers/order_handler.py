class OrderHandler:

    def process_new_order(self, new_oreder_number, redis_server) -> tuple:
        order = redis_server.get(f"order:{new_oreder_number}").decode('utf-8')
        red, green, blue, white = self.parse_order(order)
        print('red:', red, '\ngreen:', green,
              '\nblue:', blue, '\nwhite:', white)
        return tuple(map(int, (red, green, blue, white, order)))

    def process_new_disassemble_order(self, new_disoreder_number, redis_server):
        return redis_server.get(f"disorder:{new_disoreder_number}").decode('utf-8')

    def parse_order(self, order) -> tuple:
        parsed_order = [int(a) for a in str(order)]
        if len(parsed_order) == 4:
            return (parsed_order[0], parsed_order[1], parsed_order[2], parsed_order[3])
        elif len(parsed_order) == 3:
            return (0, parsed_order[0], parsed_order[1], parsed_order[2])
        elif len(parsed_order) == 2:
            return (0, 0, parsed_order[0], parsed_order[1])
        elif len(parsed_order) == 1:
            return (0, 0, 0, parsed_order[0])
