import httpx
import time
import orjson

from rich import print

import utils
import config

from context import Chat
from ._base import LlmProvider, LlmResponse, ToolCall

_client = httpx.Client(timeout=config.TIMEOUT_LLM_BASIC)


class OpenRouterLlm(LlmProvider):
    def respond(self, chat: Chat) -> LlmResponse:
        req = dict(
            url="https://openrouter.ai/api/v1/responses",
            json={
                **chat.inject(),
                "model": config.MODEL_LLM_BASIC,
                "max_tokens": config.MODEL_LLM_BASIC_MAX_TOKENS,
                "temperature": config.MODEL_LLM_BASIC_TEMPERATURE,
                "provider": {
                    "sort": "latency",
                },
                "tools": self.tools,
            },
            headers={"Authorization": f"Bearer {utils.get_env('OPENROUTER_KEY')}"},
        )

        if config.MODEL_LLM_BASIC_REASONING:
            req["json"]["reasoning"] = {
                "effort": config.MODEL_LLM_BASIC_REASONING,
            }

        with open(f"logs/{time.time()}-request.json", "wb") as f:
            req_safe = req.copy()
            req_safe["headers"] = {"_redacted_": "REDACTED"}

            f.write(orjson.dumps(req_safe, option=orjson.OPT_INDENT_2))

        response: httpx.Response = _client.post(**req)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            try:
                error_details = response.json()
                print(f"[red]ERROR: LLM call failed: {error_details}[/red]")
            except Exception:
                print(f"[red]ERROR: LLM call failed: {e}[/red]")
            raise

        cost_usd = response.json().get("usage", {}).get("total_cost_usd", 0)
        if cost_usd > config.PRICE_WARNING:
            print(f"[yellow]WARN: LLM call cost: ${cost_usd:.4f}[/yellow]")

        with open(f"logs/{time.time()}-response.json", "wb") as f:
            f.write(orjson.dumps(response.json(), option=orjson.OPT_INDENT_2))

        text = None
        for item in response.json()["output"]:
            if item["type"] == "message":
                text = item["content"][0]["text"]

        tool_calls = []
        for item in response.json()["output"]:
            if item["type"] == "function_call":
                tool_calls.append(
                    ToolCall(
                        name=item["name"],
                        args=orjson.loads(item["arguments"]),
                        call_id=item["call_id"],
                    )
                )

        return LlmResponse(
            text=text,
            tool_calls=tool_calls,
        )


if __name__ == "__main__":
    start = time.time()

    print(OpenRouterLlm().respond(Chat()))
    print(f"LLM response time: {time.time() - start:.2f}s")
