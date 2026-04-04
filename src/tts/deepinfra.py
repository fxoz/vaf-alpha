import io
import base64
import time

import httpx
import soundfile as sf
import sounddevice as sd

import utils
from ._base import TtsProvider

_client = httpx.Client(timeout=60.0)


class DeepInfraTts(TtsProvider):
    def say(self, text: str) -> None:
        start = time.time()

        res = _client.post(
            "https://api.deepinfra.com/v1/inference/hexgrad/Kokoro-82M",
            headers={
                "Authorization": f"Bearer {utils.get_env('DEEPINFRA_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "preset_voice": ["af_heart"],
                "output_format": "opus",
            },
        )
        res.raise_for_status()
        print(f"TTS inference took {time.time() - start:.2f} seconds")
        audio_b64 = res.json()["audio"].split(",", 1)[1]

        data, samplerate = sf.read(io.BytesIO(base64.b64decode(audio_b64)))

        sd.play(data, samplerate, blocking=True)
