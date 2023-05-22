import socket
import threading
import os
import json
import argparse
from queue import Queue


class IncorrectArgs(Exception):
    pass


class ClientThread(threading.Thread):
    def __init__(self, client, thread_id, lock, queue):
        super().__init__()
        self.client = client
        self.id = thread_id
        self.locker = lock
        self.queue = queue

    def run(self):
        while True:

            try:
                client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if not self.locker.locked():
                    self.locker.acquire()
                client_sock.connect(("localhost", 9090))

            except (
                    ConnectionRefusedError,
                    ConnectionAbortedError,
                    ConnectionResetError
            ):
                return self.run()

            while True:

                # self.locker.acquire()
                url = self.queue.get()

                if url is None:
                    self.queue.task_done()
                    client_sock.close()
                    return
                try:
                    # SENDING
                    client_sock.sendall(url.encode())
                    if self.locker.locked():
                        self.locker.release()

                    # RECEIVING
                    response = client_sock.recv(4096).decode()
                    print(json.loads(response))

                except (socket.error, ConnectionAbortedError, RuntimeError):
                    break
            client_sock.close()


class Client:

    def __init__(self, num_threads, url_file):
        self.num_threads = num_threads
        self.PATH = url_file
        self.lock = threading.Lock()
        self.queue = Queue()

    def start(self):
        self.read_urls()
        threads = []
        for i in range(self.num_threads):
            thread = ClientThread(self, i + 1, self.lock, self.queue)
            thread.start()
            threads.append(thread)
        # for thread in threads:
        #     thread.join()

    def read_urls(self):
        # print('обращаемся к генератору')
        with open(self.PATH, 'r') as file:
            for url in file:
                self.queue.put(url.strip())


def get_args():
    parser = argparse.ArgumentParser(description='Клиент для обкачки юрлов')
    parser.add_argument('threads', type=int, help='Количество потоков')
    parser.add_argument('url_file', type=str, help='Файл с урлами')
    args = parser.parse_args()
    if args.threads <= 0:
        raise IncorrectArgs("установите корректные аргументы клиента")
    if not os.path.exists(args.url_file):
        raise IncorrectArgs("Установите корректные аргументы клиента")
    return args.threads, args.url_file


def main():
    threads, URL_file = get_args()
    client = Client(threads, URL_file)
    client.start()


if __name__ == '__main__':
    main()
