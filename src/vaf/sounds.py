import ctypes
from pathlib import Path

winmm = ctypes.windll.winmm


def _mci(cmd: str) -> None:
    err = winmm.mciSendStringW(cmd, None, 0, None)
    if err != 0:
        buf = ctypes.create_unicode_buffer(256)
        winmm.mciGetErrorStringW(err, buf, 256)
        raise RuntimeError(f"MCI error {err}: {buf.value}")


def play_mp3(path: str, alias: str = "bgm") -> None:
    p = Path(path).resolve()
    try:
        _mci(f"close {alias}")
    except RuntimeError:
        pass

    _mci(f'open "{p}" type mpegvideo alias {alias}')
    _mci(f"play {alias}")


def stop_mp3(alias: str = "bgm") -> None:
    _mci(f"stop {alias}")
    _mci(f"close {alias}")
