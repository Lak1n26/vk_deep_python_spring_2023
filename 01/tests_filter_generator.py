import unittest
import io
from filter_generator import filt_generator, IncorrectInput


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
        self.io_file = io.StringIO()
        self.io_file.write(
            "А роза упала на лапу Азора\nМастер жрет сам\nМастер орет сам\n"
            "Лида ланцет отец наладил\nКактус тест"
        )

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

    def test_filt_generator_with_io_file(self):
        self.assertEqual(
            list(filt_generator(self.io_file, self.words)), self.expected_answer
        )
        self.assertEqual(list(filt_generator(self.io_file, ["hello", "world"])), [])
        self.assertEqual(list(filt_generator(self.io_file, [])), [])

    def test_filt_generator_with_empty_io_file(self):
        empty_io_file = io.StringIO()
        self.assertEqual(list(filt_generator(empty_io_file, self.words)), [])
        self.assertEqual(list(filt_generator(empty_io_file, [])), [])

    def test_filt_generator_incorrect_input(self):
        with self.assertRaises(IncorrectInput) as atr_err:
            list(filt_generator(123, []))
        self.assertEqual(
            "Enter the correct file name or file object", str(atr_err.exception)
        )
        with self.assertRaises(IncorrectInput) as atr_err:
            list(filt_generator(["some list"], []))
        self.assertEqual(
            "Enter the correct file name or file object", str(atr_err.exception)
        )


if __name__ == "__main__":
    unittest.main()
