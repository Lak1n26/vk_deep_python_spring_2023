import unittest
import json
from unittest.mock import MagicMock
from unittest import mock
from faker import Faker
from json_parser import parse_json


class TestJsonParser(unittest.TestCase):
    def setUp(self):
        self.json = '{"keyword1": "cat dog bad"}'
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
        self.assertEqual(
            parse_json(self.json, ["keyword1", "keyword2"], ["dog", "cow"], None), None
        )

    def test_keyword_callback(self):
        self.keyword_callback.return_value = len(["keyword1", "dog"])
        self.assertEqual(
            parse_json(self.json, ["keyword1"], ["dog"], self.keyword_callback),
            [self.keyword_callback.return_value],
        )

        self.keyword_callback.return_value = sorted(["cat", "keyword1"])
        self.assertEqual(
            parse_json(self.json, ["keyword1"], ["cat", "cow"], self.keyword_callback),
            [self.keyword_callback.return_value],
        )

        expected_calls = [
            mock.call(["keyword1", "dog"]),
            mock.call(["keyword1", "cat"]),
        ]
        self.assertEqual(expected_calls, self.keyword_callback.mock_calls)

    def test_parse_json_with_factory_boy(self):
        self.keyword_callback.return_value = "".join(["Factory", "text"])
        self.assertEqual(
            parse_json(
                self.fake_json, ["country", "text"], ["Factory"], self.keyword_callback
            ),
            [self.keyword_callback.return_value],
        )
        self.assertEqual(
            [mock.call(["text", "Factory"])], self.keyword_callback.mock_calls
        )


if __name__ == "__main__":
    unittest.main()
