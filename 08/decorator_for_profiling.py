import cProfile
import pstats
from functools import wraps


def profile_deco(func):
    profiler = cProfile.Profile()

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = profiler.runcall(func, *args, **kwargs)
        return result

    def print_stat():
        stats = pstats.Stats(profiler)
        print(f"for function - {func.__name__}")
        stats.sort_stats("cumulative").print_stats()

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(4, 5)
add(1, 2)
sub(4, 5)

add.print_stat()

for i in range(1_000_000):
    add(i + 2, i)
    for j in range(5):
        sub(i, j)

add.print_stat()
sub.print_stat()
