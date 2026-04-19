import time
import httpx
import sounddevice as sd

import utils
from ._base import TtsProvider

client = httpx.Client(timeout=httpx.Timeout(60.0), http2=True)


class AsyncComTts(TtsProvider):
    def say(self, text: str):
        start = time.perf_counter()
        first_byte_at = None

        with client.stream(
            "POST",
            "https://api.async.com/text_to_speech/streaming",
            headers={
                "x-api-key": utils.get_env("ASYNC_KEY"),
                "version": "v1",
                "Content-Type": "application/json",
            },
            json={
                "model_id": "async_flash_v1.0",
                "transcript": text,
                "voice": {"mode": "id", "id": "9b70de3a-9a70-4a73-9fbc-ef9fca83d0dc"},
                "output_format": {
                    "container": "raw",
                    "encoding": "pcm_s16le",
                    "sample_rate": 44100,
                },
            },
        ) as response:
            response.raise_for_status()

            with sd.RawOutputStream(
                samplerate=44100,
                channels=1,
                dtype="int16",
                latency="low",
                blocksize=0,
            ) as stream:
                for chunk in response.iter_bytes(chunk_size=1024):
                    if not chunk:
                        continue
                    if first_byte_at is None:
                        first_byte_at = time.perf_counter()
                        print(f"TTFB: {(first_byte_at - start) * 1000:.0f} ms")
                    stream.write(chunk)


if __name__ == "__main__":
    AsyncComTts().say("Hello, this is a test of the Async.com streaming TTS API.")
