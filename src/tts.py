import os
import time
import httpx
import base64
import subprocess

from dotenv import load_dotenv

load_dotenv()


def say(text: str) -> None:
    start = time.time()
    res = httpx.post(
        "https://api.deepinfra.com/v1/inference/hexgrad/Kokoro-82M",
        headers={
            "Authorization": f"Bearer {os.environ['DEEPINFRA_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "preset_voice": ["af_heart"],
            "output_format": "opus",
        },
        timeout=httpx.Timeout(60.0, connect=10.0),
    )
    print(f"TTS inference took {time.time() - start:.2f} seconds")

    res.raise_for_status()
    data = res.json()

    subprocess.run(
        ["ffplay", "-autoexit", "-nodisp", "-loglevel", "quiet", "-"],
        input=base64.b64decode(data["audio"].split(",")[1]),
    )


if __name__ == "__main__":
    say("The quick brown fox jumps over the lazy dog")
