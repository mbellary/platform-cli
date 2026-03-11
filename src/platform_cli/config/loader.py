import os

from .config import CLIConfig


def load_config() -> CLIConfig:
    return CLIConfig(
        api_url=os.getenv("PLATFORM_API_URL", "http://localhost:8080"),
        api_key=os.getenv("PLATFORM_API_KEY"),
    )
