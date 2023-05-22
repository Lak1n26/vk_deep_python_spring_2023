import unittest
from lru_cache import LRUCache, BadLimitValue


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.big_cache = LRUCache(100)
        self.small_cache = LRUCache(2)

    def test_incorrect_limit(self):
        with self.assertRaises(BadLimitValue) as atr_err:
            print(LRUCache(0))
        self.assertEqual(
            "Limit must be an integer bigger than zero", str(atr_err.exception)
        )
        with self.assertRaises(BadLimitValue) as atr_err:
            print(LRUCache("12"))
        self.assertEqual(
            "Limit must be an integer bigger than zero", str(atr_err.exception)
        )

    def test_small_limit(self):
        self.small_cache.set("k1", "val1")
        self.assertEqual(self.small_cache.get("k1"), "val1")

        self.small_cache.set("k2", "val2")
        self.assertEqual(self.small_cache.get("k2"), "val2")

        self.assertEqual(self.small_cache.get("k1"), "val1")

        self.small_cache.set("k3", "val3")
        self.assertEqual(self.small_cache.get("k3"), "val3")
        self.assertEqual(self.small_cache.get("k2"), None)
        self.assertEqual(self.small_cache.get("k1"), "val1")

        self.small_cache.set("k4", "val4")
        self.assertEqual(self.small_cache.get("k1"), "val1")
        self.assertEqual(self.small_cache.get("k2"), None)
        self.assertEqual(self.small_cache.get("k3"), None)
        self.assertEqual(self.small_cache.get("k4"), "val4")

    def test_max_limit(self):
        for i in range(1, 101):
            self.big_cache.set(f"k{i}", f"val{i}")
        self.assertEqual(len(self.big_cache.dct), 100)

        self.big_cache.set("k101", "val101")
        self.assertEqual(len(self.big_cache.dct), 100)

    def test_min_limit(self):
        capacity_eq_one = LRUCache(1)

        capacity_eq_one.set("k1", "val1")
        self.assertEqual(capacity_eq_one.get("k1"), "val1")
        capacity_eq_one.set("k2", "val2")
        self.assertEqual(capacity_eq_one.get("k2"), "val2")
        self.assertEqual(capacity_eq_one.get("k1"), None)
        capacity_eq_one.set("k3", "val3")
        self.assertEqual(capacity_eq_one.get("k2"), None)
        self.assertEqual(capacity_eq_one.get("k3"), "val3")

    def test_change_value(self):
        new_cache = LRUCache(2)

        new_cache.set("k1", "val1")
        new_cache.set("k2", "val2")
        new_cache.set("k1", "new_val1")

        new_cache.set("k3", "val3")
        self.assertEqual(new_cache.get("k1"), "new_val1")
        self.assertEqual(new_cache.get("k2"), None)
        self.assertEqual(new_cache.get("k3"), "val3")


if __name__ == "__main__":
    unittest.main()
