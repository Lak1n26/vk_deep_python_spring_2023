import unittest
import json
from unittest.mock import MagicMock
from unittest import mock
from faker import Faker
from main import parse_json


class TestFunc(unittest.TestCase):
    def setUp(self):
        self.json = '{"keyword1": "cat dog bad"}'
        self.answer = "dog"
        self.keyword_callback = MagicMock()
        fake = Faker(locale="Ru_ru")
        self.fake_json = json.dumps(
            {
                "name": fake.name(),
                "address": fake.address(),
                "company": fake.company(),
                "country": fake.country(),
                "text": "Проверим работоспособность функции через Factory Boy",
            }
        )
        self.fake_answer = "Factory"

    def test_parse_json_with_none(self):
        self.assertEqual(
            parse_json(self.json, None, ["dog", "cow"], self.keyword_callback), None
        )
        self.assertEqual(
            parse_json(
                self.json, ["keyword1", "keyword2"], None, self.keyword_callback
            ),
            None,
        )

    def test_keyword_callback(self):
        self.keyword_callback.return_value = list(self.answer)
        self.assertEqual(
            parse_json(self.json, ["keyword1"], ["dog"], self.keyword_callback),
            [list(self.answer)],
        )

        self.keyword_callback.return_value = sorted(self.answer)
        self.assertEqual(
            parse_json(self.json, ["keyword1"], ["dog"], self.keyword_callback),
            [["d", "g", "o"]],
        )

        expected_calls = [mock.call("dog"), mock.call("dog")]
        self.assertEqual(expected_calls, self.keyword_callback.mock_calls)

    def test_parse_json_with_factory_boy(self):
        self.keyword_callback.return_value = len(self.fake_answer)
        self.assertEqual(
            parse_json(
                self.fake_json, ["country", "text"], ["Factory"], self.keyword_callback
            ),
            [7],
        )


if __name__ == "__main__":
    unittest.main()
