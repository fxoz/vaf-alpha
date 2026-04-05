import io
import mss
import time
import httpx
import base64
import orjson

from PIL import Image

import utils
import config

from ._base import Skill

_client = httpx.Client(timeout=config.TIMEOUT_OCR)


def _screen_to_data_url() -> str:
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[0])
        buf = io.BytesIO()
        Image.frombytes("RGB", shot.size, shot.rgb).save(
            buf, format="PNG", optimize=False
        )

    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


class OcrSkill(Skill):
    def analyze_screen(self, prompt: str = "What can be seen?") -> str:
        """Screenshots the screen and runs it through an intelligent model which can also answer questions."""
        prompt += " Unless explicitly asked, respond to only the very essential information in a very concise manner."

        image = _screen_to_data_url()
        estimated_image_size_kb = len(image) * 3 / 4 / 1024

        if estimated_image_size_kb > 10_000:  # MB
            raise ValueError(
                f"Image size ({estimated_image_size_kb:.2f} KB) is too large. Cannot process."
            )

        response = _client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {utils.get_env('OPENROUTER_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "google/gemini-3.1-flash-lite-preview",
                "reasoning": {"effort": "none"},
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image},
                            },
                        ],
                    }
                ],
            },
        )
        response.raise_for_status()

        return orjson.loads(response.content)["choices"][0]["message"]["content"]


if __name__ == "__main__":
    start = time.time()
    print(OcrSkill().analyze_screen())
    print(f"Took {time.time() - start:.2f} seconds")
