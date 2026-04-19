from ._base import Skill

import time


class DateAndTimeSkill(Skill):
    def get_unix_timestamp(self) -> int:
        """Get the current Unix timestamp."""
        return int(time.time())

    def get_human_readable_time(self) -> str:
        """Current weekday, date and time. Example output: i.e. Sun Apr  5 19:18:11 2026."""
        return time.ctime()
