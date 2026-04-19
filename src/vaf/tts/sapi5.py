import comtypes.client

from ._base import TtsProvider


class Sapi5Tts(TtsProvider):
    def say(self, text: str):
        speaker = comtypes.client.CreateObject("SAPI.SpVoice")
        speaker.Speak(text)
