import io
import unittest
from exercise2 import filt_generator


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.file_name = "ex2_test.txt"
        self.words = ["роза", "мастер", "сам", "мастер", "отец"]
        self.expected_answer = [
            "А роза упала на лапу Азора",
            "Мастер жрет сам",
            "Мастер орет сам",
            "Лида ланцет отец наладил",
        ]
        self.io_file = io.StringIO()
        self.io_file.write("x\ny\nz\nc\na")
        self.io_file2 = io.StringIO()
        self.io_file2.write("А\nроза\nупала\nна\nлапу\nАзора")

    def test_filt_generator_with_file(self):
        self.assertEqual(
            list(filt_generator(self.file_name, self.words)), self.expected_answer
        )

    def test_filt_generator_with_io(self):
        self.assertEqual(
            list(filt_generator(self.io_file, ["x", "a", "c"])), ["x", "c", "a"]
        )
        self.assertEqual(list(filt_generator(self.io_file2, ["роза"])), ["роза"])


if __name__ == "__main__":
    unittest.main()
