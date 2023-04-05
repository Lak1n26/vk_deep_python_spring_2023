import unittest
from filter_generator import filt_generator


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.file_name = "file_test_filter_generator.txt"
        self.words = ["роза", "мастер", "сам", "мастер", "отец", "кактус"]
        self.expected_answer = [
            "А роза упала на лапу Азора",
            "Мастер жрет сам",
            "Мастер орет сам",
            "Лида ланцет отец наладил",
            "Кактус тест",
        ]

    def test_filt_generator_with_file(self):
        self.assertEqual(
            list(filt_generator(self.file_name, self.words)), self.expected_answer
        )

    def test_filt_generator_with_file_cactus(self):
        self.assertEqual(
            list(filt_generator("file_test_filter_generator_cactus.txt", ["кактус"])),
            ["Кактус", "Кактус классный"],
        )

    def test_filt_generator_nothing_found(self):
        self.assertEqual(list(filt_generator(self.file_name, ["задание"])), [])
        self.assertEqual(
            list(filt_generator("file_test_filter_generator_cactus.txt", ["задание"])),
            [],
        )


if __name__ == "__main__":
    unittest.main()
