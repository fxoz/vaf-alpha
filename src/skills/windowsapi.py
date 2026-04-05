import ctypes
import time

from ._base import Skill


def _press_key(hex_key_code: int):
    ctypes.windll.user32.keybd_event(hex_key_code, 0, 0, 0)
    # absolutely minimal delay for this to work:
    time.sleep(0.005)
    ctypes.windll.user32.keybd_event(hex_key_code, 0, 0x0002, 0)


class WindowsApiSkill(Skill):
    def play_pause_media(self):
        """Pauses/resumes current media."""
        _press_key(0xB3)

    def next_track(self):
        """Skips to the next media track."""
        _press_key(0xB0)

    def previous_track(self):
        """Goes back to the previous media track."""
        _press_key(0xB1)
        _press_key(0xB1)

    def volume_up(self, amount: int = 40):
        """Increases system volume (0-100)."""
        for _ in range(amount // 2):
            _press_key(0xAF)
            time.sleep(0.05)

    def volume_down(self, amount: int = 40):
        """Decreases system volume (0-100)."""
        for _ in range(amount // 2):
            _press_key(0xAE)
            time.sleep(0.05)


if __name__ == "__main__":
    WindowsApiSkill().volume_up()
