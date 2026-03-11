import requests
from platform_cli.config.loader import load_config


class APIClient:

    def __init__(self):
        self.config = load_config()

    def get(self, path):
        return requests.get(f"{self.config.api_url}{path}")

    def post(self, path, data=None):
        return requests.post(
            f"{self.config.api_url}{path}",
            json=data,
        )
