import time

from cerebras.cloud.sdk import Cerebras

import utils
from ._base import LlmProvider, Conversation


class CerebrasLlm(LlmProvider):
    def __init__(self):
        self.client = Cerebras(api_key=utils.get_env("CEREBRAS_KEY"))

    def respond(self, messages: Conversation) -> str:
        start = time.time()
        res = self.client.chat.completions.create(
            messages=messages,
            model="gpt-oss-120b",
            stream=False,
            max_completion_tokens=1024,
            temperature=0.2,
            top_p=1,
            reasoning_effort="low",
        )

        print(f"LLM response time: {time.time() - start:.2f}s")
        return res.choices[0].message.content.strip()
