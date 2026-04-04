import json
from abc import ABC, abstractmethod
from rich import print

Conversation = list[dict[str, str]]


class ToolCall:
    def __init__(self, name: str, args: dict = None):
        self.name = name
        self.args = args

    def __str__(self):
        return f"ToolCall(name={self.name}, args={self.args})"

    def __repr__(self):
        return self.__str__()


class ToolCalls(list[ToolCall]):
    def __init__(self, from_openai_json: list[dict]):
        self.extend(
            ToolCall(
                name=call["function"]["name"],
                args=json.loads(call["function"]["arguments"]),
            )
            for call in from_openai_json
        )

    def __str__(self):
        return f"ToolCalls([{', '.join(str(call) for call in self)}])"

    def __repr__(self):
        return self.__str__()


class LlmResponse:
    def __init__(self, content: str = "", tool_calls: ToolCalls | None = None):
        self.content = content
        self.tool_calls = tool_calls or ToolCalls([])

        if not any([self.content, self.tool_calls]):
            print("[yellow]WARN: LLM response is empty[/yellow]")

    def __str__(self):
        return f"LlmResponse(content={self.content}, tool_calls={self.tool_calls})"

    def __repr__(self):
        return self.__str__()


class LlmProvider(ABC):
    def __init__(self, tools: list[dict] | None = None):
        self.tools = tools or []
        try:
            json.dumps(self.tools)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Tools must be JSON-serializable: {e}")

    @abstractmethod
    def respond(self, messages: Conversation) -> str:
        raise NotImplementedError()
