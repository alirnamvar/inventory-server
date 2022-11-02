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

    def get_disorder_number(self) -> int:
        return int(self.redis_server.get('disorderNumber').decode('utf-8'))

    def get_order_list(self) -> list:
        return self.redis_server.keys('order:*')

    def get_disorder_list(self) -> list:
        return self.redis_server.keys('disorder:*')

    def flush(self) -> None:
        MAX_ORDER = 25
        logging.info("Initiating and flushing Redis server...")
        self.redis_server.set('orderNumber', 0)
        self.redis_server.set('disorderNumber', 0)
        len_order_list = len(self.get_order_list())
        len_disorder_list = len(self.get_disorder_list())
        __order_number = int(self.get('orderNumber').decode('utf-8'))
        __disorder_number = int(self.get('disorderNumber').decode('utf-8'))
        if (__order_number != len_order_list):
            logging.info("Flushing server...")
            for i in range(1, MAX_ORDER):
                if (self.get('order:%s' % i) != None):
                    logging.info("Deleting order:%s" % i)
                    self.delete('order:%s' % i)
            logging.info("Redis Server initiated and flushed.")
            return
        logging.info("Redis Server initiated.")
