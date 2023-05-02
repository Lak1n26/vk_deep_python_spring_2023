class LRUCache:
    def __init__(self, limit=42):
        if not isinstance(limit, int) or limit <= 0:
            raise BadLimitValue("Limit must be an integer bigger than zero")
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
            return None
        node = self.dct[key]
        self._remove(node)
        self._add(node)
        return node.val

    def set(self, key, value):
        if key in self.dct:
            self._remove(self.dct[key])
        node = Node(key, value)
        self._add(node)
        self.dct[key] = node
        if len(self.dct) > self.limit:
            node = self.head.next
            self._remove(node)
            del self.dct[node.key]


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class BadLimitValue(Exception):
    pass
