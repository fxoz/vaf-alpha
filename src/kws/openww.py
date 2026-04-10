from time import monotonic

import os
import globd
import numpy as np
import sounddevice as sd
from openwakeword.model import Model


model = Model(
    wakeword_model_paths=[str("models/kws/model.onnx")],
)
WAKEWORD_LABEL = next(iter(model.models))


SAMPLE_RATE = 16000
CHUNK_SIZE = 1280
SENSITIVITY = 0.5
DETECTION_COOLDOWN_SECONDS = 1.0
last_detection_at = float("-inf")

print(f"Listening for '{WAKEWORD_LABEL}'...")


def callback(indata, frames, time, status):
    global last_detection_at

    if status:
        print(status)

    audio_frame = (indata[:, 0] * 32767).astype(np.int16)
    prediction = model.predict(audio_frame)

    now = monotonic()
    if (
        prediction[WAKEWORD_LABEL] > SENSITIVITY
        and now - last_detection_at >= DETECTION_COOLDOWN_SECONDS
    ):
        last_detection_at = now
        print("Wake word detected!")


with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    blocksize=CHUNK_SIZE,
    callback=callback,
):
    while True:
        sd.sleep(1000)
