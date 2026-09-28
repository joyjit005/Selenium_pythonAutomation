"""
Central configuration for the API Automation Framework.
Change BASE_URL here to point the whole framework at a different environment.
"""

BASE_URL = "https://jsonplaceholder.typicode.com"

# Simulated auth header - shows how a real framework would attach a token
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer dummy-test-token"
}

TIMEOUT = 10  # seconds, applied to every request
