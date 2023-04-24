import socket
import sys
import threading
import os


class IncorrectParameters(Exception):
    pass


def get_client_parameters():
    global PATH
    PATH, THREADS = None, None

    if not THREADS:
        try:
            int(sys.argv[1])
            THREADS = sys.argv[1]
        except ValueError:
            raise IncorrectParameters(
                "Введите корректное значение количества потоков"
            )

    if not PATH:
        if os.path.exists(sys.argv[2]):
            PATH = sys.argv[2]
        else:
            raise IncorrectParameters("Введите корректное название файла")

    return int(THREADS), PATH


def generator_url(sem):
    global PATH
    with sem:
        with open(PATH) as file:
            for url in file:
                yield url.strip()


def mnogopotok(THREADS, sem):
    sock = socket.socket()
    sock.connect(("localhost", 9090))
    all_threads = [
        threading.Thread(
            target=connect_and_send,
            name=f"thread_{i}_reading_and_sending_url",
            args=[sock, sem],
        )
        for i in range(THREADS)
    ]

    for th in all_threads:
        th.start()
    return all_threads


def connect_and_send(sock, sem):
    global all_urls_sent

    for url in generator_url(sem):
        if all_urls_sent:
            return
        try:
            sock.send(url.encode())
            received_data = sock.recv(1024).decode()
            print(received_data)
        except ConnectionResetError:
            return
        except ConnectionAbortedError:
            return

    all_urls_sent = True
    return


if __name__ == "__main__":
    THREADS, PATH = get_client_parameters()
    sem = threading.Semaphore(1)
    all_urls_sent = False
    mnogopotok(THREADS, sem)
