import os
from typing import TypeVar

from dotenv import load_dotenv

load_dotenv()

ProviderT = TypeVar("ProviderT")


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        raise RuntimeError(f"Environment variable {key} not set")
    return value
