import functools
import os
import threading
import time
from http import HTTPStatus
from typing import Callable
from urllib.parse import urlencode

import requests

API_KEY = os.getenv("WEATHER_API_KEY")
API_URL = "https://api.weatherapi.com/v1/current.json"

CITIES = [
    "Moscow",
    "London",
    "Phuket",
    "Ubud",
    "Zurich",
]

storage = {}
lock = threading.Lock()


def benchmark(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)

        print(func.__name__, "elapsed", time.time() - begin)

        return result

    return inner


def get_weather(city: str) -> float:
    query = urlencode(query={
        "q": city,
        "key": API_KEY
    })

    response = requests.get(url=f"{API_URL}?{query}")
    if response.status_code != HTTPStatus.OK:
        raise ValueError("Bad response from server")

    body = response.json()
    return body["current"]["temp_c"]


def add_weather_to_storage(city: str) -> None:
    value = get_weather(city)

    lock.acquire()
    storage[city] = value
    lock.release()


@benchmark
def thread_requests() -> None:
    threads = []
    for city in CITIES:
        thread = threading.Thread(target=add_weather_to_storage, args=(city,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


@benchmark
def blocked_requests() -> None:
    for city in CITIES:
        storage[city] = get_weather(city)


if __name__ == "__main__":
    thread_requests()

    storage = {}

    blocked_requests()
