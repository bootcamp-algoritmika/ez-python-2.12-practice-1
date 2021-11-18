import functools
import os
import time
from typing import Callable

API_KEY = os.getenv("WEATHER_API_KEY")
API_URL = "https://api.weatherapi.com/v1/current.json"

storage = {}


def benchmark(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)

        print(func.__name__, "elapsed", time.time() - begin)

        return result

    return inner


@benchmark
def thread_requests() -> None:
    pass


@benchmark
def blocked_requests() -> None:
    pass


if __name__ == "__main__":
    thread_requests()

    storage = {}

    blocked_requests()
