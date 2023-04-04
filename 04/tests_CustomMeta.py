import unittest
from CustomMeta import CustomClass


class TestCustomMeta(unittest.TestCase):
    def test_class_attributes(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError) as atr_err:
            CustomClass.x
        self.assertEqual(
            "type object 'CustomClass' has no attribute 'x'", str(atr_err.exception)
        )

    def test_instance_attributes(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")
        with self.assertRaises(AttributeError) as atr_err:
            inst.x
        self.assertEqual(
            "'CustomClass' object has no attribute 'x'", str(atr_err.exception)
        )
        with self.assertRaises(AttributeError) as atr_err:
            inst.val
        self.assertEqual(
            "'CustomClass' object has no attribute 'val'", str(atr_err.exception)
        )
        with self.assertRaises(AttributeError) as atr_err:
            inst.line()
        self.assertEqual(
            "'CustomClass' object has no attribute 'line'", str(atr_err.exception)
        )

    def test_added_attributes(self):
        inst = CustomClass()
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            inst.dynamic


if __name__ == "__main__":
    unittest.main()
