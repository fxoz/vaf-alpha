import os
import glob
import time
import threading
import numpy as np
import sounddevice as sd
from rich import print
from openwakeword.model import Model

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280
SENSITIVITY = 0.5
DETECTION_COOLDOWN_SECONDS = 2.0
STARTUP_IGNORE_SECONDS = 0.75

_LAST_DETECTION_AT = float("-inf")


def _find_model():
    for file in glob.glob(os.path.join("models/kws", "_*.onnx")):
        return file
    raise FileNotFoundError(
        "[bold red]No wake word model found in models/kws[/bold red]"
    )


_MODEL_FILE = _find_model()


def _make_model():
    model = Model(wakeword_model_paths=[_MODEL_FILE])
    label = next(iter(model.models))
    return model, label


def loop():
    global _LAST_DETECTION_AT

    detected = threading.Event()
    model, wakeword_label = _make_model()
    started_at = time.monotonic()

    print(f"[green]Listening for [italic]{wakeword_label}[/italic]...[/green]")

    def callback(indata: np.ndarray, frames, time_info, status):
        global _LAST_DETECTION_AT

        now = time.monotonic()

        if now - started_at < STARTUP_IGNORE_SECONDS:
            return

        if status:
            print(status)

        audio_frame = (indata[:, 0] * 32767).astype(np.int16)
        prediction = model.predict(audio_frame)
        score = prediction[wakeword_label]

        if (
            score > SENSITIVITY
            and now - _LAST_DETECTION_AT >= DETECTION_COOLDOWN_SECONDS
        ):
            _LAST_DETECTION_AT = now
            print(
                f"[yellow]Wake word detected:[/yellow] {wakeword_label} ({score:.3f})"
            )
            detected.set()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=CHUNK_SIZE,
        callback=callback,
    ):
        while not detected.is_set():
            sd.sleep(50)
