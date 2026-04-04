import os
from dotenv import load_dotenv

load_dotenv()


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Environment variable {key} not set")
    return value
