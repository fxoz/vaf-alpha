import config
import orjson

from rich import print
from typing import Union, Optional

from llm._base import Conversation


class Chat:
    def __init__(self):
        self.messages: Conversation = [
            {
                "role": "developer",
                "content": [
                    {"type": "input_text", "text": config.SYSTEM_PROMPT.strip()}
                ],
            },
        ]

        self.current_user_prompt: Optional[str] = None

    def wrap_user_prompt_with_sentinel(self, prompt: str) -> str:
        return (
            f"%% THE FOLLOWING IS THE LAST USER PROMPT TO ENSURE CONTEXT %%\n{prompt}"
        )

    def is_user_prompt_in_context(self, context: Conversation) -> bool:
        if self.current_user_prompt is None:
            return True

        return any(
            msg.get("role") == "user"
            and any(
                content.get("type") == "input_text"
                and content.get("text")
                in {
                    self.current_user_prompt,
                    self.wrap_user_prompt_with_sentinel(self.current_user_prompt),
                }
                for content in msg.get("content", [])
            )
            for msg in context
        )

    def get_context(self) -> Conversation:
        recent_limit = config.RECENT_MESSAGES_LIMIT

        context_minified: Conversation = (
            self.messages[:1] + self.messages[1:][-recent_limit:]
            if recent_limit > 0
            else self.messages[:1]
        )

        if self.current_user_prompt is not None and not self.is_user_prompt_in_context(
            context_minified
        ):
            context_minified.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": self.wrap_user_prompt_with_sentinel(
                                self.current_user_prompt
                            ),
                        },
                    ],
                }
            )

        return context_minified

    def inject(self) -> dict:
        return dict(input=self.get_context())

    def add(self, role: str, content: str) -> None:
        self.messages.append(
            {"role": role, "content": [{"type": "input_text", "text": content}]}
        )

    def add_user_message(self, content: str) -> None:
        self.current_user_prompt = content
        self.add("user", content)

    def add_ai_message(self, content: str) -> None:
        self.add("assistant", content)

    def add_tool_call(self, name: str, arguments: dict, call_id: str) -> None:
        self.messages.append(
            {
                "type": "function_call",
                "call_id": call_id,
                "name": name,
                "arguments": orjson.dumps(arguments).decode(),
            }
        )

    def add_tool_call_output(
        self, call_id: str, output: Union[dict, list, str, int, float, bool, None]
    ) -> None:
        if not isinstance(output, dict):
            output = {"result": output}

        try:
            orjson.dumps(output)
        except orjson.JSONEncodeError as e:
            raise ValueError(f"Tool output must be JSON-serializable: {e}")

        self.messages.append(
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": orjson.dumps(output).decode(),
            }
        )


if __name__ == "__main__":
    chat = Chat()
    print(chat.get_context())
