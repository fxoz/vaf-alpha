from ._base import Skill

import time


class DateAndTimeSkill(Skill):
    def get_unix_timestamp(self) -> int:
        """Get the current Unix timestamp."""
        return int(time.time())

    def get_human_readable_time(self) -> str:
        """Get the current time in a human-readable format."""
        return time.ctime()
