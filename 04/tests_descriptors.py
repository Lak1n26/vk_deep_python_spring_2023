import unittest
from descriptors import Company, IncorrectType


class TestDescriptors(unittest.TestCase):
    def setUp(self):
        self.comp1 = Company(70, "SBER", 212.0)

    def test_share_amount(self):
        self.assertEqual(self.comp1.amount, 70)
        self.comp1.amount = 71
        self.assertEqual(self.comp1.amount, 71)
        self.comp1.amount = 0
        self.assertEqual(self.comp1.amount, 0)

        with self.assertRaises(IncorrectType) as inc_type:
            self.comp1.amount = -10
        self.assertTrue("-10" in str(inc_type.exception))
        self.assertEqual(self.comp1.amount, 0)

        del self.comp1.amount
        with self.assertRaises(AttributeError) as atr_err:
            print(self.comp1.amount)
        self.assertEqual(
            "'Company' object has no attribute '_int_field_amount'",
            str(atr_err.exception),
        )

    def test_company_name(self):
        self.assertEqual(self.comp1.name, "SBER")
        self.comp1.name = "GAZP"
        self.assertEqual(self.comp1.name, "GAZP")

        with self.assertRaises(IncorrectType) as inc_type:
            self.comp1.name = 123
        self.assertTrue("123" in str(inc_type.exception))
        self.assertEqual(self.comp1.name, "GAZP")

        with self.assertRaises(IncorrectType) as inc_type:
            self.comp1.name = "123"
        self.assertTrue("123" in str(inc_type.exception))
        self.assertEqual(self.comp1.name, "GAZP")

        with self.assertRaises(IncorrectType) as inc_type:
            self.comp1.name = "sber"
        self.assertTrue("sber" in str(inc_type.exception))
        self.assertEqual(self.comp1.name, "GAZP")

        with self.assertRaises(IncorrectType) as inc_type:
            self.comp1.name = ""
        self.assertTrue("" in str(inc_type.exception))
        self.assertEqual(self.comp1.name, "GAZP")

        del self.comp1.name
        with self.assertRaises(AttributeError) as atr_err:
            print(self.comp1.name)
        self.assertEqual(
            "'Company' object has no attribute '_str_field_name'",
            str(atr_err.exception),
        )

    def test_share_price(self):
        self.assertEqual(self.comp1.price, 212.0)
        self.comp1.price = 100
        self.assertEqual(self.comp1.price, 100.0)
        self.comp1.price = 1.1
        self.assertEqual(self.comp1.price, 1.1)

        with self.assertRaises(IncorrectType) as inc_type:
            self.comp1.price = 0
        self.assertTrue("0" in str(inc_type.exception))
        self.assertTrue(self.comp1.price, 1.1)

        with self.assertRaises(IncorrectType) as inc_type:
            self.comp1.price = "some_str"
        self.assertTrue("some_str" in str(inc_type.exception))
        self.assertTrue(self.comp1.price, 1.1)

        del self.comp1.price
        with self.assertRaises(AttributeError) as atr_err:
            print(self.comp1.price)
        self.assertEqual(
            "'Company' object has no attribute '_positive_number_field_price'",
            str(atr_err.exception),
        )


if __name__ == "__main__":
    unittest.main()
