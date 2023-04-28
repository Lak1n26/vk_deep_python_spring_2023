import unittest
import subprocess
import time
from unittest.mock import AsyncMock
import sys
import fetcher


class FetcherTests(unittest.TestCase):
    def test_get_parameters(self):
        sys.argv = ["fetcher.py", "abc", "URLS.txt"]
        with self.assertRaises(fetcher.IncorrectParameters):
            fetcher.get_parametrs()

        sys.argv = ["fetcher.py", "1", "URLS"]
        with self.assertRaises(fetcher.IncorrectParameters):
            fetcher.get_parametrs()

        sys.argv = ["fetcher.py", "10", "URLS.txt"]
        THREADS, PATH = fetcher.get_parametrs()
        self.assertEqual((THREADS, PATH), (10, "URLS.txt"))

        sys.argv = ["fetcher.py", "-c", "10", "URLS.txt"]
        THREADS, PATH = fetcher.get_parametrs()
        self.assertEqual((THREADS, PATH), (10, "URLS.txt"))

    def test_fetcher_time(self):
        def time_with_10_threads():
            t1 = time.time()
            subprocess.run(["python", "fetcher.py", "10", "URLS.txt"])
            t2 = time.time()
            return t2 - t1

        def time_with_1_thread():
            t1 = time.time()
            subprocess.run(["python", "fetcher.py", "2", "URLS.txt"])
            t2 = time.time()
            return t2 - t1

        self.assertTrue(time_with_10_threads() < time_with_1_thread())

    def test_generator_url(self):
        PATH = "URLS.txt"
        expected_answer = [
            "https://ru.wikipedia.org/wiki/Python",
            "https://ru.wikipedia.org/wiki/Haskell",
            "https://ru.wikipedia.org/wiki/C%2B%2B",
            "https://ru.wikipedia.org/wiki/Java",
            "https://ru.wikipedia.org/wiki/Perl",
            "https://ru.wikipedia.org/wiki/Object_Pascal",
            "https://ru.wikipedia.org/wiki/C_Sharp",
            "https://ru.wikipedia.org/wiki/Kotlin",
            "https://ru.wikipedia.org/wiki/JavaScript",
            "https://ru.wikipedia.org/wiki/Ruby",
            "https://ru.wikipedia.org/wiki/ECMAScript",
            "https://ru.wikipedia.org/wiki/TypeScript",
            "https://ru.wikipedia.org/wiki/CoffeeScript",
        ]
        self.assertEqual(list(fetcher.generator_url(PATH)), expected_answer)


class FetchURLTest(unittest.IsolatedAsyncioTestCase):
    async def test_mocking_fetch_url(self):
        fetcher.fetch_url = AsyncMock()
        fetcher.fetch_url.return_value = "success fetched url"
        self.assertEqual("success fetched url", await fetcher.fetch_url())


class FetchSeveralURLsTest(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_several_urls(self):
        my_mock = unittest.mock.AsyncMock()
        fetcher.fetch_several_urls = my_mock
        fetcher.fetch_several_urls.return_value = "success"
        await fetcher.fetch_several_urls(10, "URLS.txt")
        await fetcher.fetch_several_urls(1, "URLS.txt")
        expected_calls = [
            unittest.mock.call(10, "URLS.txt"),
            unittest.mock.call(1, "URLS.txt"),
        ]
        self.assertEqual(expected_calls, fetcher.fetch_several_urls.mock_calls)


if __name__ == "__main__":
    unittest.main()
