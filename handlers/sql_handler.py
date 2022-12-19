import logging
import mysql.connector
from mysql.connector import connect, errorcode
from constants import WAREHOUSE_TABLE_DESCRIPTION, DISASSEMBLE_ORDERS_TABLE_DESCRIPTION

class SQLHandler:

    def __init__(self, server, user, database):
        self.host = server
        self.user = user
        self.database = database
        self._connect_to_server()
        self.create_tables([WAREHOUSE_TABLE_DESCRIPTION,
                    DISASSEMBLE_ORDERS_TABLE_DESCRIPTION])

    def create_tables(self, list_of_table_description):
        created_tables = []
        cursor1 = self.return_new_cursor()
        cursor1.execute("show tables;")
        counter = 0
        for (table,) in cursor1:
            counter += 1
            cursor2 = self.return_new_cursor()
            cursor2.execute(f"DROP TABLE {table};")
            cursor2.close()
        cursor1.close()
        if counter != 0:
            logging.info(f"{counter} existing table has erased!")
        for table_description in list_of_table_description:
            table_name = (table_description.split(" ")[6]).split('\n')[0]
            cursor = self.return_new_cursor()
            try:
                cursor.execute(table_description)
                created_tables.append(table_name)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    logging.warning("This SQL table already exists.")
                else:
                    logging.error(err.msg)
            cursor.close()
        if len(created_tables) != 0:
            logging.info(f"Created tables: {str(created_tables).replace('[', '').replace(']', '')}")

    def del_pallet_record_in_warehouse(self, pallet_positon):
        cursor = self.return_new_cursor()
        delete_query = f"DELETE FROM warehouse WHERE position = {pallet_positon}"
        cursor.execute(delete_query)
        # logging.info(f"Pallet row {pallet_positon} deleted from 'warehouse' table of SQL server.")
        self.__cnx.commit()
        cursor.close()

    def update_disassemble_orders_table(self, disorder_number, position):
        cursor = self.return_new_cursor()
        query = f"INSERT INTO disassemble_orders (disorder_number, position)" + \
                f"VALUES ({disorder_number}, {position})"
        cursor.execute(query)
        # logging.info("Disassemble order saved into 'disassemble_orders' table of SQL server.")
        self.__cnx.commit()
        cursor.close()

    def update_warehouse_table(self, pallet_materials : tuple, position : int) -> None:
        cursor = self.return_new_cursor()
        query = f"INSERT INTO warehouse (position, red, green, blue, white)" + \
                f"VALUES ({position}, {pallet_materials[0]}, {pallet_materials[1]}, \
                {pallet_materials[2]}, {pallet_materials[3]})"
        cursor.execute(query)
        logging.info("Components and positon of pallet saved into 'warehouse' table of SQL server.")
        self.__cnx.commit()
        cursor.close()

    def return_new_cursor(self):
        return self.__cnx.cursor(buffered=True)

    def _connect_to_server(self):
        try:
            self.__cnx = connect(user=self.user,
                                host=self.host,
                                database=self.database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database does not exist")
            else:
                logging.error(err)