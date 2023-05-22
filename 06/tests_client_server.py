import unittest
import sys
import threading
import subprocess
import client
import server
import socket
import json
from unittest.mock import MagicMock, patch


class TestClient(unittest.TestCase):
    def test_get_client_args(self):
        sys.argv = ["client.py", "10", "URLS.txt"]
        self.assertEqual((10, "URLS.txt"), client.get_args())

        with self.assertRaises(client.IncorrectArgs) as inc_file:
            sys.argv = ["client.py", "11", "not_existing_file"]
            client.get_args()
        self.assertTrue(
            "Установите корректные аргументы клиента", str(inc_file.exception)
        )

        with self.assertRaises(client.IncorrectArgs) as inc_threads:
            sys.argv = ["client.py", "0", "100URLS.txt"]
            client.get_args()
        self.assertTrue(
            "Установите корректные аргументы клиента",
            str(inc_threads.exception)
        )

    def test_client_queue(self):
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
        some_client = client.Client(10, "URLS.txt")
        some_client.read_urls()
        self.assertEqual(list(some_client.queue.queue), expected_answer)
        self.assertEqual(some_client.queue.get(), expected_answer[0])
        self.assertEqual(some_client.queue.get(), expected_answer[1])

    def test_client_start(self):
        self.client = client.Client(2, 'URLS.txt')
        self.thread = client.ClientThread(
            MagicMock(),
            1,
            MagicMock(),
            MagicMock()
        )

        threads = [self.thread, self.thread]
        with patch.object(
                client.ClientThread,
                'start',
                MagicMock()
        ) as start_mock:
            with patch('builtins.range', return_value=range(2)):
                with patch('client.ClientThread', side_effect=threads):
                    self.client.start()
                    self.assertEqual(start_mock.call_count, 2)


class TestServer(unittest.TestCase):

    def setUp(self):
        self.master = server.Master(2, 5)
        self.client_sock = MagicMock(spec=socket.socket)
        self.worker = server.Worker(self.master, 1, MagicMock())

    def test_get_server_args(self):
        sys.argv = ["server.py", "-w", "12", "-k", "7"]
        self.assertEqual((12, 7), server.get_args())

        with self.assertRaises(server.IncorrectArgs) as err:
            sys.argv = ["server.py", "-w", "0", "-k", "5"]
            server.get_args()
        self.assertTrue(
            "Установите корректные аргументы сервера", str(err.exception)
        )

        with self.assertRaises(server.IncorrectArgs) as err:
            sys.argv = ["server.py", "-w", "15", "-k", "-2"]
            server.get_args()
        self.assertTrue(
            "Установите корректные аргументы сервера", str(err.exception)
        )

    def test_server_accept_client(self):
        with patch(
                'socket.socket.accept',
                return_value=(self.client_sock, 'address')
        ):
            result = self.master.accept_client()
            self.assertEqual(result, self.client_sock)

    def test_get_url(self):
        url = "https://ru.wikipedia.org/wiki/Python"
        self.client_sock.recv.return_value = url.encode()
        result = self.worker.master.get_url(self.client_sock)
        self.assertEqual(result, url)

    def test_process_url(self):
        url = "https://ru.wikipedia.org/wiki/Python"
        count_words = "{'word1': 40, 'word2': 25, 'word3': 12}"
        return_val = json.dumps(url + ': ' + count_words)
        with patch('server.Worker.process_url', return_value=return_val):
            fetched_url = self.worker.process_url(url)
            self.assertEqual(
                json.loads(fetched_url),
                "https://ru.wikipedia.org/wiki/Python: "
                "{'word1': 40, 'word2': 25, 'word3': 12}"
            )

    def test_send_result(self):
        result = 'some result'
        locker = MagicMock()
        self.master.send_result(self.client_sock, result, locker)
        self.client_sock.send.assert_called_once_with(result.encode())
        locker.release.assert_called_once()
        self.assertEqual(self.master.urls_fetched, 1)


class TestFULL(unittest.TestCase):
    def test_server_client_with_100_urls(self):
        def run_client():
            subprocess.run(["python", "client.py", "10", "100URLS.txt"])

        def run_server():
            print("Проверка сервер-клиент на файле со 100 URL'ами")
            subprocess.run(["python", "server.py", "-w", "10", "-k", "7"])
        threading.Thread(target=run_server).start()
        threading.Thread(target=run_client).start()


if __name__ == "__main__":
    unittest.main()
