import requests
from datetime import timedelta

URL = "http://127.0.0.1:8000/blog/5/"

def mean_time_of_load(n: int, url: str):
    elapsed = timedelta()
    for _ in range(n):
        elapsed += requests.get(url).elapsed
    return elapsed.total_seconds() / n

print(f"Mean loading time of {URL} with caching is", mean_time_of_load(100, URL) * 1000, 'ms')