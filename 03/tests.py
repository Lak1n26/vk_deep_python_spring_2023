import unittest
from CustomList import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self):
        self.lst1 = CustomList([5, 1, 3, 7])
        self.lst2 = CustomList([1, 2, 7])
        self.lst3 = CustomList([1])
        self.lst4 = CustomList([2, 5])
        self.lst5 = [2, 5]
        self.lst6 = CustomList([1])

    def test_add(self):
        self.assertEqual(self.lst1 + self.lst2, CustomList([6, 3, 10, 7]))
        self.assertEqual(self.lst3 + self.lst4, CustomList([3, 5]))
        self.assertEqual(self.lst6 + self.lst5, CustomList([3, 5]))

    def test_radd(self):
        self.assertEqual(self.lst5 + self.lst4, CustomList([4, 10]))
        self.assertEqual(self.lst5 + self.lst6, CustomList([3, 5]))

    def test_sub(self):
        self.assertEqual(self.lst1 - self.lst2, CustomList([4, -1, -4, 7]))
        self.assertEqual(self.lst3 - self.lst4, CustomList([-1, -5]))
        self.assertEqual(self.lst6 - self.lst5, CustomList([-1, -5]))

    def test_rsub(self):
        self.assertEqual(self.lst5 - self.lst6, CustomList([1, 5]))
        self.assertEqual(self.lst5 - self.lst4, CustomList([0, 0]))

    def test_eq(self):
        self.assertFalse(self.lst1 == self.lst2)
        self.assertFalse(self.lst3 == self.lst4)
        self.assertTrue(self.lst3 == self.lst6)

    def test_ne(self):
        self.assertTrue(self.lst1 != self.lst2)
        self.assertTrue(self.lst3 != self.lst4)
        self.assertFalse(self.lst3 != self.lst6)

    def test_gt(self):
        self.assertTrue(self.lst1 > self.lst2)
        self.assertTrue(self.lst4 > self.lst3)
        self.assertTrue(self.lst2 > self.lst6)

    def test_ge(self):
        self.assertTrue(self.lst1 >= self.lst2)
        self.assertTrue(self.lst3 >= self.lst6)
        self.assertFalse(self.lst3 >= self.lst4)

    def test_lt(self):
        self.assertFalse(self.lst1 < self.lst2)
        self.assertFalse(self.lst4 < self.lst3)
        self.assertTrue(self.lst3 < self.lst2)

    def test_le(self):
        self.assertTrue(self.lst2 <= self.lst1)
        self.assertFalse(self.lst4 <= self.lst3)
        self.assertTrue(self.lst3 <= self.lst6)

    def test_str(self):
        self.assertEqual(str(self.lst1), "[5, 1, 3, 7], сумма = 16")
        self.assertEqual(str(self.lst2), "[1, 2, 7], сумма = 10")
        self.assertEqual(str(self.lst3), "[1], сумма = 1")


if __name__ == "__main__":
    unittest.main()
