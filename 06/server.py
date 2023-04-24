import sys
import threading
import socket
import queue
from collections import Counter
import requests
from bs4 import BeautifulSoup


NEED_TO_GET = 4


class IncorrectParameters(Exception):
    pass


def get_args():
    w, k = None, None
    for i, arg in enumerate(sys.argv):
        if arg == "-w" and sys.argv[i + 1].isnumeric():
            w = sys.argv[i + 1]
        if arg == "-k" and sys.argv[i + 1].isnumeric():
            k = sys.argv[i + 1]
    if not w:
        if sys.argv[1].isnumeric():
            w = sys.argv[1]
        else:
            raise IncorrectParameters("установите параметры -w и -k")
    if not k:
        if sys.argv[2].isnumeric():
            k = sys.argv[2]
        else:
            raise IncorrectParameters("установите параметры -w и -k")
    return int(w), int(k)


class Master:
    q = queue.Queue()
    some_url = "some url"

    def __init__(self, w, k):
        self.w = w
        self.k = k

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(("localhost", 9090))
        self.server_sock.listen()
        self.server_sock.settimeout(10)

    def create_threads(self, w):
        for i in range(w):
            Master.q.put(
                threading.Thread(
                    target=fetch_and_send,
                    name=f"worker_{i}_fetching_url"
                )
            )

    def run_server(self):
        global NEED_TO_GET
        total_urls = 0
        client_sock, _ = self.server_sock.accept()
        self.create_threads(self.w)

        while True:
            if total_urls >= NEED_TO_GET:
                break
            while True:
                data = client_sock.recv(4096)
                if data:
                    url = data.decode()
                    curr_thread = Master.q.get()
                    curr_thread._kwargs = {
                        "url": url,
                        "client_sock": client_sock,
                        "k": self.k,
                    }
                    if not curr_thread.is_alive():
                        curr_thread.start()
                        curr_thread = threading.Thread(
                            target=fetch_and_send, name=curr_thread.name
                        )
                    Master.q.put(curr_thread)
                    total_urls += 1
                    print(f"Всего отработано: {total_urls} URL'ов")
                    break


def fetch_and_send(url, client_sock, k):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    text = " ".join(soup.stripped_strings)
    words = text.lower().split()
    word_counts = Counter(words)
    answer = {}
    for word, count in word_counts.most_common(k):
        answer[word] = count
    message = f"{url} : {answer}"
    client_sock.sendall(message.encode())


if __name__ == "__main__":
    w, k = get_args()
    master = Master(w, k)
    master.run_server()
