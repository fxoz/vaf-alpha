from skills.dateandtime import DateAndTimeSkill
from skills.memory import MemorySkill
from skills.ocr import OcrSkill
from skills.spotify import SpotifySkill
from skills.windowsapi import WindowsApiSkill

# Configure enabled skill instances here.
SKILLS = [
    OcrSkill(),
    MemorySkill(),
    DateAndTimeSkill(),
    WindowsApiSkill(),
    # SpotifySkill(),
]
