import unittest
from unittest import mock
from predictor import SomeModel, predict_message_mood


class TestPredictor(unittest.TestCase):
    def setUp(self):
        self.test_model = SomeModel()
        self.mock_model = mock.Mock(spec=SomeModel)

    def test_predict(self):
        self.assertEqual(self.test_model.predict("random text bla-bla"), 1)

        with mock.patch("predictor.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 3.14
            self.assertEqual(self.test_model.predict("pi"), 3.14)
            self.assertEqual([mock.call("pi")], mock_predict.mock_calls)

            mock_predict.return_value = 1e6
            self.assertEqual(self.test_model.predict("wanna larger"), 1000000.0)
            expected_calls = [mock.call("pi"), mock.call("wanna larger")]
            self.assertEqual(expected_calls, mock_predict.mock_calls)

    def test_predict_message_mood_different_borders(self):
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
        self.assertEqual(
            predict_message_mood("feel the border", self.test_model),
            "отл",
        )

    def test_model_predict(self):
        self.mock_model.predict.return_value = 2
        self.assertEqual(predict_message_mood("val=2", self.mock_model), "отл")

        self.mock_model.predict.return_value = 0.5
        self.assertEqual(predict_message_mood("val=0.5", self.mock_model), "норм")

        self.mock_model.predict.return_value = 0.5
        self.assertEqual(
            predict_message_mood(
                "val=0.5 and change borders", self.mock_model, 1.5, 10
            ),
            "неуд",
        )

        expected_calls = [
            mock.call("val=2"),
            mock.call("val=0.5"),
            mock.call("val=0.5 and change borders"),
        ]
        self.assertEqual(expected_calls, self.mock_model.predict.mock_calls)


if __name__ == "__main__":
    unittest.main()
