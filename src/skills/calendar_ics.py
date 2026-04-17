import ics
import requests

from rich import print
from datetime import datetime, timezone

import utils


def fetch_ics_url(ics_url: str):
    calendar = ics.Calendar(requests.get(ics_url).text)
    events = sorted(calendar.events, key=lambda event: event.begin or "")

    if not events:
        raise RuntimeError(f"No events found in ICS feed: {ics_url}")

    today = datetime.now(timezone.utc)
    events = [event for event in events if event.begin and event.begin >= today]

    for event in events[-5:]:
        print(f"[bold]{event.begin}[/bold] {event.name}")

    event = events[0]
    open("logs/calendar.ics", "w", encoding="utf-8").write(
        f"{event.name}\n{event.begin}\n{event.end}\n{event.description or '- No description - '}\n{event.location}\n{event.url}\n{event.categories}"
    )


if __name__ == "__main__":
    fetch_ics_url(utils.get_calendars()[0])
