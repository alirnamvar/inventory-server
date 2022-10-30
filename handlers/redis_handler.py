import redis
import logging


class RedisHandler:
    redis_server = None

    def __init__(self, *, server, port) -> None:
        self.server = server
        self.port = port
        self._make_connection()

    def _make_connection(self) -> None:
        self.redis_server = redis.Redis(host=self.server, port=self.port, db=0)

    def get_connection_status(self) -> bool:
        return self.redis_server.ping()

    def get(self, key: str) -> str:
        return self.redis_server.get(key)

    def set(self, key: str, value: str) -> None:
        self.redis_server.set(key, value)

    def delete(self, key: str) -> None:
        self.redis_server.delete(key)

    def get_order_number(self) -> int:
        return int(self.redis_server.get('orderNumber').decode('utf-8'))

    def get_order_list(self) -> list:
        return self.redis_server.keys('order:*')

    def flush(self) -> None:
        """flush previous orders in redis server and set orderNumber to 0

        Args:
            redis_server (RedisHandler): a redis server
        """
        logging.info("Initiating and flushing server...")
        self.redis_server.set('orderNumber', 0)
        len_order_list = len(self.get_order_list())
        __order_number = int(self.get(
            'orderNumber').decode('utf-8'))
        if (__order_number != len_order_list):
            logging.info("Flushing server...")
            for i in range(1, 20):
                if (self.get('order:%s' % i) != None):
                    logging.info("Deleting order:%s" % i)
                    self.delete('order:%s' % i)
            logging.info("Server initiated and flushed.")
            return
        logging.info("Server initiated.")
