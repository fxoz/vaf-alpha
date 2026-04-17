import os
from dotenv import load_dotenv

load_dotenv()


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Environment variable {key} not set")
    return value


def get_calendars() -> list[str]:
    calendars = get_env("CALENDARS_ICS")
    return calendars.split(" ")
