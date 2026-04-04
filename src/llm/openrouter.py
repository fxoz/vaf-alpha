import httpx

import time
import utils
from rich import print
from ._base import LlmProvider, Conversation, LlmResponse, ToolCalls

_client = httpx.Client(timeout=60.0)


class OpenRouterLlm(LlmProvider):
    def respond(self, messages: Conversation) -> LlmResponse:
        response: httpx.Response = _client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json={
                "model": "openai/gpt-oss-safeguard-20b",
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.2,
                "provider": {
                    "sort": "latency",
                },
                "reasoning": {
                    "effort": "minimal",
                },
                "tools": self.tools,
            },
            headers={"Authorization": f"Bearer {utils.get_env('OPENROUTER_KEY')}"},
        )
        response.raise_for_status()

        cost_usd = response.json().get("usage", {}).get("total_cost_usd", 0)
        if cost_usd > 0.01:
            print(f"[yellow]WARN: LLM call cost: ${cost_usd:.4f}[/yellow]")

        return LlmResponse(
            content=response.json()["choices"][0]["message"]["content"],
            tool_calls=ToolCalls(
                response.json()["choices"][0]["message"].get("tool_calls", [])
            ),
        )


if __name__ == "__main__":
    start = time.time()
    print(OpenRouterLlm().respond([{"role": "user", "content": "what's up?"}]))
    print(f"LLM response time: {time.time() - start:.2f}s")
