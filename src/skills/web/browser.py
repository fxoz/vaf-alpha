from camoufox.sync_api import Camoufox

import httpx
import tempfile
import base64
import os

import utils
import config

from PIL import Image, ImageDraw

_client = httpx.Client(timeout=config.TIMEOUT_OCR)


def analyze_screen(image_data_url: str, prompt: str) -> str:
    # prompt += " Unless explicitly asked, respond to only the very essential information in a very concise manner."

    response = _client.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {utils.get_env('OPENROUTER_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.MODEL_OCR,
            "reasoning": {"effort": "none"},
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data_url},
                        },
                    ],
                }
            ],
        },
    )
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


with Camoufox() as browser:
    page = browser.new_page()
    page.goto("https://www.wetteronline.de/")
    page.wait_for_load_state("domcontentloaded")

    fd, tmp_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)

    try:
        page.screenshot(path=tmp_path)

        with open(tmp_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        data_url = f"data:image/png;base64,{encoded}"

        dimensions = Image.open(tmp_path).size
        print(f"Image dimensions: {dimensions}")

        result = analyze_screen(
            data_url,
            prompt=f"""What position should the cursor click next in order to enter the city or region?
If there is a cookie or consent banner, find the accept button instead!
IMPORTANT: Image dimensions: {dimensions}.
Respond with the coordinates in the exact format x,y. NEVER anything else. 0,0 = top left.""",
        )
        print(result)

        image = Image.open(tmp_path)
        draw = ImageDraw.Draw(image)
        x, y = map(int, result.split(","))
        radius = 5
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="red")
        image.show()
        image.save("debug.png")

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
