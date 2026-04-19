import os

from rich import print
from dotenv import load_dotenv

load_dotenv()


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Environment variable {key} not set")
    return value


def get_calendars() -> dict[str, str]:
    calendars = get_env("CALENDARS_ICS")

    calendar_dict = {}
    for calendar in calendars.split(";"):
        if not calendar.strip():
            continue
        name, url = calendar.strip().split(" ", 1)
        calendar_dict[name] = url

    return calendar_dict
