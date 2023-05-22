import threading
import socket
from collections import Counter
import argparse
import json
import requests
from bs4 import BeautifulSoup


class IncorrectArgs(Exception):
    pass


def get_args():
    parser = argparse.ArgumentParser(
        description='Сервер для обкачки набора урлов'
    )
    parser.add_argument(
        '-w',
        type=int,
        help='количество воркеров')
    parser.add_argument(
        '-k',
        type=int,
        help='количество самых популярных слов')
    args = parser.parse_args()
    if args.w <= 0 or args.k <= 0:
        raise IncorrectArgs("Установите корректные аргументы сервера")
    return args.w, args.k


class Worker(threading.Thread):
    def __init__(self, master, thread_id, lock):
        super().__init__()
        self.master = master
        self.id = thread_id
        self.lock = lock

    def run(self):
        while True:
            try:
                if not self.lock.locked():
                    self.lock.acquire()
                client_sock = self.master.accept_client()
                if client_sock is None:
                    break
                if self.lock.locked():
                    self.lock.release()

            except Exception:  # в случае непредвиденной ошибки
                return self.run()
            while True:
                try:
                    if not self.lock.locked():
                        self.lock.acquire()
                    url = self.master.get_url(client_sock)
                    if self.lock.locked():
                        self.lock.release()

                    result = self.process_url(url)

                    self.master.send_result(client_sock, result, self.lock)
                # except KeyboardInterrupt:
                #     sys.exit()
                except Exception:  # в случае непредвиденной ошибки
                    break

    def process_url(self, url):
        # message = f"{url} : success"  # test
        # time.sleep(3 % self.id + 1)  # test
        # return json.dumps(message)  # test

        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = " ".join(soup.stripped_strings)
        words = text.lower().split()
        word_counts = Counter(words)
        answer = {}
        for word, count in word_counts.most_common(self.master.k):
            answer[word] = count
        message = f"{url} : {answer}"
        return json.dumps(message)


class Master:
    def __init__(self, w, k):

        self.w = w
        self.k = k
        self.urls_fetched = 0
        self.lock = threading.Lock()

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(("localhost", 9090))
        self.server_sock.listen(self.w)
        self.server_sock.settimeout(5)

    def run_server(self):
        self.start_workers()

    def accept_client(self):
        client_sock, _ = self.server_sock.accept()
        return client_sock

    def get_url(self, client_sock):
        while True:
            url = client_sock.recv(4096).decode()
            if len(url) > 0:
                return url

    def start_workers(self):
        workers = []
        for i in range(self.w):
            worker = Worker(self, i + 1, self.lock)
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()

    def send_result(self, client_sock, result, locker):

        client_sock.send(result.encode())
        if not locker.locked():
            locker.acquire()
        self.urls_fetched += 1
        locker.release()
        print(f"Всего обработано: {self.urls_fetched} урлов")


def main():
    w, k = get_args()
    server = Master(w, k)
    server.run_server()


if __name__ == "__main__":
    main()
