import json
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4.1-mini"

TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Use tools when needed. "
    "When a tool result is provided, answer the user directly."
)


def get_weather(location: str, unit: str = "celsius") -> dict:
    fake_db = {
        "berlin": {"temp_c": 13, "condition": "Cloudy"},
        "paris": {"temp_c": 16, "condition": "Sunny"},
    }

    rec = fake_db.get(location.strip().lower(), {"temp_c": 20, "condition": "Unknown"})
    temp = rec["temp_c"]
    if unit == "fahrenheit":
        temp = round(temp * 9 / 5 + 32, 1)

    return {
        "location": location,
        "unit": unit,
        "temperature": temp,
        "condition": rec["condition"],
    }


def build_manual_context(user_message: str, compact_history: list[dict]) -> list[dict]:
    """
    compact_history is a manually managed list of prior items/messages you decided to keep.
    """
    return [
        {
            "role": "developer",
            "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
        },
        *compact_history,
        {"role": "user", "content": [{"type": "input_text", "text": user_message}]},
    ]


def first_turn(user_message: str):
    input_items = build_manual_context(user_message, compact_history=[])

    response = client.responses.create(
        model=MODEL,
        tools=TOOLS,
        input=input_items,
    )

    return response


def continue_after_tool(response, compact_history: list[dict]):
    """
    Takes a response that contains a function call, executes it,
    then makes a second manual request without previous_response_id.
    """
    function_calls = [item for item in response.output if item.type == "function_call"]
    if not function_calls:
        return response, compact_history

    # For simplicity, handle one tool call here
    call = function_calls[0]
    args = json.loads(call.arguments)

    if call.name == "get_weather":
        tool_result = get_weather(**args)
    else:
        tool_result = {"error": f"Unknown tool: {call.name}"}

    # Keep only the minimal context we care about
    # 1) original user turn
    # 2) assistant function_call item
    # 3) tool output item
    new_history = compact_history.copy()

    # include the assistant function_call as an input item next turn
    new_history.append(
        {
            "type": "function_call",
            "call_id": call.call_id,
            "name": call.name,
            "arguments": call.arguments,
        }
    )

    # include the tool result as an input item next turn
    new_history.append(
        {
            "type": "function_call_output",
            "call_id": call.call_id,
            "output": json.dumps(tool_result),
        }
    )

    followup = client.responses.create(
        model=MODEL,
        tools=TOOLS,
        input=[
            {
                "role": "developer",
                "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
            },
            *new_history,
        ],
    )

    return followup, new_history


if __name__ == "__main__":
    # Step 1: user asks something
    r1 = first_turn("What's the weather in Berlin in fahrenheit?")

    # Step 2: model may call tool; we execute locally and continue manually
    r2, history = continue_after_tool(r1, compact_history=[])

    print(r2.output_text)
