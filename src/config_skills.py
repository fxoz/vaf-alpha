from skills.dateandtime import DateAndTimeSkill
from skills.memory import MemorySkill
from skills.ocr import OcrSkill
from skills.windowsapi import WindowsApiSkill

ocr = OcrSkill()
memory = MemorySkill()
date_and_time = DateAndTimeSkill()
windows_api = WindowsApiSkill()

SKILLS = [ocr, memory, date_and_time, windows_api]

TOOL_REGISTRY = {
    "DateAndTimeSkill__get_human_readable_time": date_and_time.get_human_readable_time,
    "DateAndTimeSkill__get_unix_timestamp": date_and_time.get_unix_timestamp,
    "MemorySkill__list_all": memory.list_all,
    "MemorySkill__write": memory.write,
    "MemorySkill__read": memory.read,
    "WindowsApiSkill__play_pause_media": windows_api.play_pause_media,
    "WindowsApiSkill__next_track": windows_api.next_track,
    "WindowsApiSkill__previous_track": windows_api.previous_track,
    "WindowsApiSkill__volume_up": windows_api.volume_up,
    "WindowsApiSkill__volume_down": windows_api.volume_down,
    "OcrSkill__analyze_screen": ocr.analyze_screen,
}
