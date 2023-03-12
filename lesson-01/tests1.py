import unittest
from unittest import mock
from exercise1 import SomeModel
from exercise1 import predict_message_mood


class TestModel(unittest.TestCase):
    def setUp(self):
        self.test_model = SomeModel()

    def test_predict(self):
        self.assertEqual(self.test_model.predict("random text bla-bla"), 1)

        with mock.patch("exercise1.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 3.14
            self.assertEqual(self.test_model.predict("pi"), 3.14)
            self.assertEqual([mock.call("pi")], mock_predict.mock_calls)

            mock_predict.return_value = 1e6
            self.assertEqual(self.test_model.predict("wanna larger"), 1000000.0)
            expected_calls = [mock.call("pi"), mock.call("wanna larger")]
            self.assertEqual(expected_calls, mock_predict.mock_calls)

    def test_predict_message_mood(self):
        self.assertEqual(predict_message_mood("default values", self.test_model), "отл")
        self.assertEqual(
            predict_message_mood("bigger values", self.test_model, 2.5, 5), "неуд"
        )
        self.assertEqual(
            predict_message_mood("smaller values", self.test_model, 0.00001, 0.0002),
            "отл",
        )
        self.assertEqual(
            predict_message_mood("large values", self.test_model, 50000, 1000000),
            "неуд",
        )
        self.assertEqual(
            predict_message_mood("feel the border", self.test_model, 0.99999, 1.00001),
            "норм",
        )


if __name__ == "__main__":
    unittest.main()
