import os
import time
import asyncio
import argparse
import aiohttp


class IncorrectArgs(Exception):
    pass


def get_parametrs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'threads',
        type=int,
        help='Количество одновременных запросов'
    )
    parser.add_argument(
        'url_file',
        type=str,
        help="Файл с URL'ами"
    )
    args = parser.parse_args()
    if args.threads <= 0:
        raise IncorrectArgs(
            "Установите корректное количество одновременных запросов"
        )
    if not os.path.exists(args.url_file):
        raise IncorrectArgs("Установите корректное название файла с URL'ами")
    return args.threads, args.url_file


def generator_url(PATH):
    with open(PATH, encoding='utf-8') as file:
        for url in file:
            yield url.strip()


async def fetch_url(sem, session, url, counter):
    async with sem:
        async with session.get(url) as resp:
            if resp.status != 200:
                print(f"{url} - ошибка открытия")
                return
            counter['processed'] += 1
            await asyncio.sleep(0.001)
            # можно выводить статистику по обработанным урлам с каждым десятком
            # if counter['processed'] % 10 == 0:
            #     print(f"обработано: {counter['processed']}")


async def fetch_several_urls(THREADS, PATH):
    t1 = time.time()
    sem = asyncio.Semaphore(THREADS)
    counter = {'processed': 0}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in generator_url(PATH):
            task = asyncio.create_task(fetch_url(sem, session, url, counter))
            tasks.append(task)
        await asyncio.gather(*tasks)
    t2 = time.time()
    time_spent = t2 - t1
    return counter['processed'], time_spent

if __name__ == "__main__":
    THREADS, PATH = get_parametrs()
    loop = asyncio.get_event_loop()
    result, time_spent = loop.run_until_complete(
        fetch_several_urls(THREADS, PATH)
    )
    print(f"Обработано всего: {result} url'ов")
    print(f"Заняло времени: {time_spent} сек")
