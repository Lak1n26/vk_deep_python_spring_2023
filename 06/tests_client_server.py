import unittest
import sys
import threading
import subprocess
import client
import server

class ClientServerTests(unittest.TestCase):
    def setUp(self):
        server.Master.NEED_TO_GET = 20
        sys.argv = ["client.py", "12", "URLS.txt"]
        self.THREADS, self.PATH = client.get_client_parameters()
        self.sem = threading.Semaphore(1)

    def test_get_client_parameters(self):
        sys.argv = ["client.py", "12", "URLS.txt"]
        self.assertEqual(client.get_client_parameters(), (12, "URLS.txt"))

        sys.argv = ["client.py", "1", "URLS.txt"]
        self.assertEqual(client.get_client_parameters(), (1, "URLS.txt"))

        with self.assertRaises(client.IncorrectParameters) as inc_args:
            sys.argv = ["client.py", "aaaaaa", "URLS.txt"]
            client.get_client_parameters()
        self.assertTrue(
            "Введите корректное значение количества потоков" in str(inc_args.exception)
        )

        with self.assertRaises(client.IncorrectParameters) as inc_args:
            sys.argv = ["client.py", "12", "some_non_existent_file.txt"]
            client.get_client_parameters()
        self.assertTrue("Введите корректное название файла" in str(inc_args.exception))

    def test_get_server_parameters(self):
        sys.argv = ["server.py", "-w", "1", "-k", "1"]
        self.assertEqual(server.get_args(), (1, 1))

        sys.argv = ["server.py", "1", "1"]
        self.assertEqual(server.get_args(), (1, 1))

        sys.argv = ["server.py", "1", "1"]
        self.assertEqual(server.get_args(), (1, 1))

        sys.argv = ["server.py", "-w", "1", "1"]
        self.assertEqual(server.get_args(), (1, 1))

        sys.argv = ["server.py", "1", "-k", "1"]
        self.assertEqual(server.get_args(), (1, 1))

        with self.assertRaises(server.IncorrectParameters) as inc_args:
            sys.argv = ["server.py", "a", "b"]
            server.get_args()
        self.assertTrue(
            "установите параметры -w и -k" in str(inc_args.exception)
        )

    def test_client_generator_url(self):
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
        self.assertEqual(list(client.generator_url(self.sem)), expected_answer)

    def test_server_client_100_urls(self):
        def run_client():
            subprocess.run(["python", "client.py", "2", "100URLS.txt"])

        def run_server(URLS):
            print("Проверка сервер-клиент на файле со 100 URL'ами")
            sys.argv = ["server.py", "-w", "2", "-k", "7"]
            w, k = server.get_args()
            master = server.Master(w, k)
            server.NEED_TO_GET = URLS
            master.run_server()

        threading.Thread(target=run_server, args=[10]).start()
        threading.Thread(target=run_client).start()


if __name__ == "__main__":
    unittest.main()
