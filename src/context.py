import config
import orjson

from llm._base import Conversation
from typing import Union


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

    def get_context(self) -> Conversation:
        return self.messages[:1] + self.messages[1:][-config.RECENT_MESSAGES_LIMIT :]

    def inject(self) -> dict:
        return dict(input=self.get_context())

    def add(self, role: str, content: str) -> None:
        self.messages.append(
            {"role": role, "content": [{"type": "input_text", "text": content}]}
        )

    def add_user_message(self, content: str) -> None:
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
