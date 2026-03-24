import time

from cerebras.cloud.sdk import Cerebras

from .base import LlmProvider
import utils


class CerebrasLlm(LlmProvider):
    provider_name = "cerebras"

    def __init__(self):
        self.client = Cerebras(api_key=utils.get_env("CEREBRAS_KEY"))

    def respond(self, text: str) -> str:
        start = time.time()
        res = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Answer in a very concise manner. NEVER use markdown, emojis, lists, asterisks, emphasis, code blocks, or ANY kind of formatting! This is extremely important, just write plain text for Text-to-Speech! Unless explicitly asked, respond with a few short sentences at most!",
                },
                {"role": "user", "content": text},
            ],
            model="gpt-oss-120b",
            stream=False,
            max_completion_tokens=1024,
            temperature=0.2,
            top_p=1,
            reasoning_effort="medium",
        )

        print(f"LLM response time: {time.time() - start:.2f}s")
        return res.choices[0].message.content.strip()


def respond(text: str) -> str:
    return CerebrasLlm().respond(text)


if __name__ == "__main__":
    print(respond("Say something interesting about the world."))
