import unittest
from unittest.mock import AsyncMock
from unittest import mock
import sys
import asyncio
import fetcher


class FetcherTests(unittest.TestCase):
    def test_get_parameters(self):
        sys.argv = ["fetcher.py", "-2", "URLS.txt"]
        with self.assertRaises(fetcher.IncorrectArgs):
            fetcher.get_parametrs()

        sys.argv = ["fetcher.py", "1", "URLS"]
        with self.assertRaises(fetcher.IncorrectArgs):
            fetcher.get_parametrs()

        sys.argv = ["fetcher.py", "10", "URLS.txt"]
        THREADS, PATH = fetcher.get_parametrs()
        self.assertEqual((THREADS, PATH), (10, "URLS.txt"))

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


class TestFetchlURL(unittest.TestCase):
    async def mock_response(self, status):
        response = mock.Mock()
        response.status = status
        return response

    async def test_fetch_url_success(self):
        url = "https://ru.wikipedia.org/wiki/Python"
        sem = asyncio.Semaphore(5)
        counter = {"processed": 0}

        session = AsyncMock()
        session.return_value = await self.mock_response(200)

        await fetcher.fetch_url(sem, session, url, counter)

        self.assertEqual(counter["processed"], 1)
        session.get.assert_called_once_with(url)

    async def test_fetch_url_failure(self):
        url = "https://ru.wikipedia.org/wiki/Python"
        sem = asyncio.Semaphore(5)
        counter = {"processed": 0}

        session = AsyncMock()
        session.get.return_value = await self.mock_response(404)

        await fetcher.fetch_url(sem, session, url, counter)

        self.assertEqual(counter["processed"], 0)
        session.get.assert_called_once_with(url)

        # проверка что в консоль вывелось сообщение с ошибкой
        print.assert_called_once_with(f"{url} - ошибка открытия")


class TestFetchSeveralURLs(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_several_urls(self):
        THREADS = 5
        PATH = "URLS.txt"

        sem_mock = AsyncMock()
        response = AsyncMock()
        response.status.return_value = 200
        session_mock = AsyncMock()
        session_mock.get.return_value.__aenter__.return_value = response
        counter = {"processed": 0}
        expected_processed = 3

        async def fetch_url_mock(sem, session, url, counter):
            counter["processed"] += 1

        generator_url_mock = mock.Mock()
        generator_url_mock.return_value = [
            "https://ru.wikipedia.org/wiki/Python",
            "https://ru.wikipedia.org/wiki/C%2B%2B",
            "https://ru.wikipedia.org/wiki/TypeScript",
        ]

        with mock.patch("asyncio.Semaphore", sem_mock), mock.patch(
            "aiohttp.ClientSession", return_value=session_mock
        ), mock.patch("fetcher.fetch_url", fetch_url_mock), mock.patch(
            "fetcher.generator_url", generator_url_mock
        ):
            total_fetched, time_spent = await fetcher.fetch_several_urls(THREADS, PATH)
            print(f"Всего обработано = {total_fetched}")
            self.assertEqual(
                total_fetched, expected_processed
            )  # проверка, что обработалось именно 3 урла
            self.assertGreater(
                time_spent, 0
            )  # проверка, что время выполнения больше нуля
            generator_url_mock.assert_called_once_with(PATH)
            sem_mock.assert_called_once_with(5)


if __name__ == "__main__":
    unittest.main()
