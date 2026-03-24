import json
import time

import httpx

from .base import AsrProvider
import utils


class MistralAsr(AsrProvider):
    provider_name = "mistral"

    def __init__(self):
        self.url = "https://api.mistral.ai/v1/audio/transcriptions"

    def transcribe(self, file_path: str) -> str:
        start = time.time()
        with (
            open(file_path, "rb") as f,
            httpx.stream(
                "POST",
                self.url,
                headers={
                    "Authorization": f"Bearer {utils.get_env('MISTRAL_KEY')}",
                    "Accept": "text/event-stream",
                },
                data={"model": "voxtral-mini-latest", "stream": "true"},
                files={"file": (file_path, f)},
                timeout=httpx.Timeout(60.0, connect=10.0),
            ) as r,
        ):
            r.raise_for_status()
            for line in r.iter_lines():
                if line.startswith("data:"):
                    msg = json.loads(line[5:].strip())
                    if msg.get("type") == "transcription.done":
                        print(f"ASR took {time.time() - start:.2f}s")
                        return msg["text"]
        raise RuntimeError("No transcription received")


if __name__ == "__main__":
    asr = MistralAsr()
    print(asr.transcribe("low.opus"))
