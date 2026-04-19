import ics
import time
import httpx

from rich import print
from models import CalendarEvent
from datetime import datetime, timezone, timedelta

import utils
import config

from ._base import Skill

_CLIENT = httpx.Client(timeout=10)


class CalendarSkill(Skill):
    def __init__(self):
        self._last_refresh = 0.0
        self._ics_calendar_names_and_urls: dict[str, str] = utils.get_calendars()

        self.all_events = []
        self.refresh_calendars()

    def fetch_calendar(self, ics_url: str, name: str) -> list[ics.Event]:
        calendar = ics.Calendar(_CLIENT.get(ics_url).text)
        events = sorted(calendar.events, key=lambda event: event.begin or "")
        print(f"[blue]Fetched {len(events)} events from ICS calendar '{name}'[/blue]")

        if not events:
            raise RuntimeError(f"No events found in ICS feed: {ics_url}")
        return events

    def refresh_calendars(self):
        if time.monotonic() - self._last_refresh < config.CALENDAR_CACHE_SECONDS:
            print("[yellow]Using cached calendar data...[/yellow]")
            return

        for name, url in self._ics_calendar_names_and_urls.items():
            try:
                events = self.fetch_calendar(url, name)

                # turn into our own format and add calendar name to each event
                events = [
                    CalendarEvent(
                        name=event.name,
                        begin=event.begin.astimezone(timezone.utc)
                        if event.begin
                        else None,
                        end=event.end.astimezone(timezone.utc) if event.end else None,
                        categories=list(event.categories) if event.categories else [],
                        description=event.description or "",
                        location=event.location or "",
                        url=event.url or "",
                        calendar_name=name,
                    )
                    for event in events
                ]

                self.all_events.extend(events)
                self._last_refresh = time.monotonic()
            except Exception as e:
                print(f"[red]Error fetching calendar '{name}': {e}[/red]")

    def fetch_upcoming_events(self):
        self.refresh_calendars()

        open("logs/calendar_raw.txt", "w", encoding="utf-8").write(str(self.all_events))

        today = datetime.now(timezone.utc)
        max_timeframe = today + timedelta(days=config.CALENDAR_CONTEXT_MAX_DAYS)

        print(f"Total events: {len(self.all_events)}")
        print(
            f"Num of events with begin time: {len([event for event in self.all_events if event.begin])}"
        )
        print(
            f"Num of events AFTER today: {len([event for event in self.all_events if event.begin and event.begin >= today])}"
        )
        print(
            f"Num of events within timeframe: {len([event for event in self.all_events if event.begin and event.begin >= today and event.begin <= max_timeframe])}"
        )

        relevant_events = [
            event
            for event in self.all_events
            if event.begin and event.begin >= today and event.begin <= max_timeframe
        ][: config.CALENDAR_CONTEXT_MAX_ITEMS]

        print(f"Relevant events: {len(relevant_events)}")

        text = ""
        for event in relevant_events:
            print(f"[bold]{event.begin} @ {event.calendar_name}[/bold] {event.name}")
            text += f"{event.name} --- {event.begin} - {event.end} --- {event.categories} --- {event.description[:50].replace('\n', ' ') or '- No description - '} --- @ {event.location} --- {event.url} --- \n"

        open("logs/calendar.txt", "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    skill = CalendarSkill()
    print(skill.fetch_upcoming_events())
