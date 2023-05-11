import logging
import sys


def set_logger(stdo, filt):
    format_sentry = logging.Formatter(
        "%(asctime)s\t%(levelname)s\t[stdout]\t%(message)s"
    )
    format_example = logging.Formatter(
        "%(asctime)s\t%(levelname)s\t[file]\t%(message)s"
    )

    fake_sentry = logging.StreamHandler()
    fake_sentry.setLevel(logging.WARNING)
    fake_sentry.setFormatter(format_sentry)

    default_log = logging.FileHandler("logs.log")
    default_log.setLevel(logging.INFO)
    default_log.setFormatter(format_example)

    full = logging.getLogger("full")
    full.setLevel(logging.INFO)
    full.addHandler(default_log)
    if filt:
        full.addFilter(NoDraftFilter())
    if stdo:
        full.addHandler(fake_sentry)
    return logging.getLogger("full")


class NoDraftFilter(logging.Filter):
    def filter(self, record):
        return "значен" not in record.msg


class LRUCache:
    def __init__(self, limit=42):
        if not isinstance(limit, int) or limit <= 0:
            logger.error("Ошибка создания LRUCache с параметром "
                         "limit = %s типа %s", limit, type(limit))
            raise BadLimitValue("Limit must be an integer bigger than zero")
        logger.info("был создан новый LRUCache")
        self.limit = limit
        self.dct = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, node):
        prev_new_node = self.tail.prev
        prev_new_node.next = node
        node.prev = prev_new_node
        self.tail.prev = node
        node.next = self.tail

    def _remove(self, node):
        node_prev = node.prev
        node_next = node.next
        node_prev.next = node_next
        node_next.prev = node_prev

    def get(self, key):
        if key not in self.dct:
            logger.info("ключ %s отсутствует в словаре", key)
            return None
        node = self.dct[key]
        self._remove(node)
        self._add(node)
        logger.info("по ключу %s получено значение %s", key, node.val)
        return node.val

    def set(self, key, value):
        if key in self.dct:
            logger.warning("замена значения существующего "
                           "ключа %s на %s", key, value)
            self._remove(self.dct[key])
        else:
            logger.info("установка значения %s отсутствующего "
                        "ключа %s", value, key)
        node = Node(key, value)
        self._add(node)
        self.dct[key] = node
        if len(self.dct) > self.limit:
            node = self.head.next
            self._remove(node)
            logger.warning("установлен предел! Значение по ключу %s "
                           "равное %s было удалено!",
                           node.key, self.dct[node.key].val)
            del self.dct[node.key]


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class BadLimitValue(Exception):
    pass


if __name__ == '__main__':
    STDO = "-s" in sys.argv
    FILT = "-f" in sys.argv
    logger = set_logger(STDO, FILT)

    logger.info("stdout = %s", STDO)
    logger.info("filter = %s", FILT)
    small_cache = LRUCache(2)
    small_cache.set("k1", "val1")
    small_cache.get("k1")
    small_cache.get("k2")
    small_cache.set("k2", "val2")
    small_cache.get("k2")
    small_cache.set("k3", "val3")
    small_cache.get("k3")
    small_cache.set("k3", "new_val3")

    try:
        error_cache = LRUCache('10')
    except BadLimitValue:
        pass
