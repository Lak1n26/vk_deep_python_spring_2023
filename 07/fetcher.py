import sys
import os
import asyncio
import aiohttp


class IncorrectParameters(Exception):
    pass


def get_parametrs():
    THREADS, PATH = None, None
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-c" and sys.argv[i + 1].isnumeric():
            THREADS = int(sys.argv[i + 1])
        if os.path.exists(sys.argv[i]):
            PATH = sys.argv[i]
    if not THREADS:
        try:
            THREADS = int(sys.argv[1])
        except Exception:
            raise IncorrectParameters(
                "Введите корректное число одновременных запросов"
            )
    if not PATH:
        raise IncorrectParameters("Введите корректный путь до файла с URL'ами")
    return THREADS, PATH


def generator_url(PATH):
    with open(PATH) as file:
        for url in file:
            yield url.strip()


async def fetch_url(sem, session, url):
    async with sem:
        async with session.get(url) as resp:
            assert resp.status == 200


async def fetch_several_urls(THREADS, PATH):
    sem = asyncio.Semaphore(THREADS)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in generator_url(PATH):
            task = asyncio.create_task(fetch_url(sem, session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    THREADS, PATH = get_parametrs()
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(fetch_several_urls(THREADS, PATH))
