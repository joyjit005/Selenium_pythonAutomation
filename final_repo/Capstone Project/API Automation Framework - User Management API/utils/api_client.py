"""
Reusable API client - wraps the `requests` library so every step
definition talks to one place instead of calling requests.* directly.
This is the core "framework" piece: swap BASE_URL in config.py and
every test still works.
"""

import requests
from config.config import BASE_URL, HEADERS, TIMEOUT


class APIClient:
    def __init__(self, base_url=BASE_URL, headers=None):
        self.base_url = base_url
        self.headers = headers or HEADERS

    def get(self, endpoint, params=None):
        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            params=params,
            timeout=TIMEOUT,
        )

    def post(self, endpoint, data=None):
        return requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=data,
            timeout=TIMEOUT,
        )

    def put(self, endpoint, data=None):
        return requests.put(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=data,
            timeout=TIMEOUT,
        )

    def delete(self, endpoint):
        return requests.delete(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            timeout=TIMEOUT,
        )
