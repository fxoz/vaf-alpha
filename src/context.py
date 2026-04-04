from llm._base import Conversation

conversation: Conversation = [
    {
        "role": "system",
        "content": """Answer in a very concise manner.
NEVER use markdown, emojis, lists, asterisks, emphasis, code blocks, or ANY kind of formatting!
This is extremely important, just write plain text for Text-to-Speech!
Unless explicitly asked, respond with 1-2 very short sentences at most!""",
    },
]


def get() -> Conversation:
    return conversation[:1] + conversation[-4:]


def add(role: str, content: str) -> None:
    conversation.append({"role": role, "content": content})


def add_user(content: str) -> None:
    add("user", content)


def add_ai(content: str) -> None:
    add("assistant", content)
