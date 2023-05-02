import unittest
from custom_meta import CustomClass


class TestCustomMeta(unittest.TestCase):
    def test_class_attributes(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError) as atr_err:
            print(CustomClass.x)
        self.assertEqual(
            "type object 'CustomClass' has no attribute 'x'",
            str(atr_err.exception)
        )

    def test_instance_attributes(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")
        with self.assertRaises(AttributeError) as atr_err:
            print(inst.x)
        self.assertEqual(
            "'CustomClass' object has no attribute 'x'", str(atr_err.exception)
        )
        with self.assertRaises(AttributeError) as atr_err:
            print(inst.val)
        self.assertEqual(
            "'CustomClass' object has no attribute 'val'",
            str(atr_err.exception)
        )
        with self.assertRaises(AttributeError) as atr_err:
            inst.line()
        self.assertEqual(
            "'CustomClass' object has no attribute 'line'",
            str(atr_err.exception)
        )

    def test_added_attributes(self):
        inst = CustomClass()
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            print(inst.dynamic)

    def test_invalid_value(self):
        inst = CustomClass()

        self.assertEqual(inst.custom_x, 50)
        inst.custom_x = 5000
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_custom_x, 5000)

        self.assertEqual(inst.custom_line(), 100)
        inst.custom_line = lambda: 5000
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(inst.custom_custom_line(), 5000)

        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        inst.dynamic = "some changes"
        self.assertEqual(inst.custom_dynamic, "added later")


if __name__ == "__main__":
    unittest.main()
