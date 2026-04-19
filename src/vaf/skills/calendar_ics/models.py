from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


@dataclass
class Repetition:
    frequency: Enum = Enum("Frequency", "DAILY WEEKLY MONTHLY YEARLY")
    interval: int = 1  # e.g. every 2 days
    until: datetime | None = None  # end date for the repetition


@dataclass
class CalendarEvent:
    name: str
    begin: datetime | None
    end: datetime | None
    categories: list[str]
    description: str
    location: str
    url: str
    calendar_name: str
