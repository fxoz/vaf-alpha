import os
import json
import httpx

from dotenv import load_dotenv

load_dotenv()


def transcribe(file_path: str) -> str:
    with (
        open(file_path, "rb") as f,
        httpx.stream(
            "POST",
            "https://api.mistral.ai/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {os.environ['MISTRAL_KEY']}",
                "Accept": "text/event-stream",
            },
            data={"model": "voxtral-mini-latest", "stream": "true"},
            files={"file": (file_path, f)},
            timeout=httpx.Timeout(60.0, connect=10.0),
        ) as r,
    ):
        r.raise_for_status()
        for line in r.iter_lines():
            if line and line.startswith("data:"):
                msg = json.loads(line[5:].strip())
                if msg.get("type") == "transcription.done":
                    return msg["text"]
    raise RuntimeError("No final transcription received")


if __name__ == "__main__":
    print(transcribe("low.opus"))
