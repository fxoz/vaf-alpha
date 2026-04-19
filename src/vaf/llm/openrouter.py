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
    def _calculate_usage(self, data: dict) -> None:
        usage = data.get("usage") or {}
        is_byok = usage.get("is_byok", False)

        if usage.get("cost") == 0 and is_byok:
            cost_details = usage.get("cost_details") or {}
            cost_usd = cost_details.get(
                "upstream_inference_cost",
                usage.get("upstream_inference_cost", 0),
            )
        else:
            cost_usd = usage.get("cost", 0)

        if cost_usd > config.PRICE_WARNING:
            print(
                f"[yellow]WARN! LLM call cost: ${cost_usd:.4f} @ {data.get('usage', {}).get('input_tokens', 0)} input tokens[/yellow]{' [byok]' if is_byok else ''}"
            )

    def respond(self, chat: Chat) -> LlmResponse:
        provider_config = dict(sort="latency")
        if config.MODEL_LLM_BASIC_OPENROUTER_ENFORCE_PROVIDERS:
            provider_config["order"] = (
                config.MODEL_LLM_BASIC_OPENROUTER_ENFORCE_PROVIDERS
            )

        req = dict(
            url="https://openrouter.ai/api/v1/responses",
            json={
                **chat.inject(),
                "model": config.MODEL_LLM_BASIC,
                "max_tokens": config.MODEL_LLM_BASIC_MAX_TOKENS,
                "temperature": config.MODEL_LLM_BASIC_TEMPERATURE,
                "provider": provider_config,
                "tools": self.tools,
            },
            headers={"Authorization": f"Bearer {utils.get_env('OPENROUTER_KEY')}"},
        )

        if config.MODEL_LLM_BASIC_REASONING:
            req["json"]["reasoning"] = {
                "effort": config.MODEL_LLM_BASIC_REASONING,
            }

        self._log_request(req)

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

        data = response.json()

        if not isinstance(data, dict) or "output" not in data:
            print(f"[red]ERROR: Unexpected LLM response format: {response.text}[/red]")
            raise ValueError("Unexpected LLM response format")

        self._calculate_usage(data)

        with open(f"logs/{time.time()}-response.json", "wb") as f:
            f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))

        text = None
        tool_calls = []
        for item in data["output"]:
            if item["type"] == "message":
                text = item["content"][0]["text"]

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
