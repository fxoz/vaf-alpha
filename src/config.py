from skills.memory import MemorySkill
from skills.dateandtime import DateAndTimeSkill

TOOL_REGISTRY = {
    "DateAndTimeSkill__get_human_readable_time": DateAndTimeSkill().get_human_readable_time,
    "DateAndTimeSkill__get_unix_timestamp": DateAndTimeSkill().get_unix_timestamp,
    "MemorySkill__list_all": MemorySkill().list_all,
    "MemorySkill__write": MemorySkill().write,
    "MemorySkill__read": MemorySkill().read,
}


# For every LLM call, we include the initial system prompt + the most recent N messages in the conversation history.
# Low values save tokens -> money, but may reduce response quality/accuracy. Very high values (e.g., 10 or more) may be unnecessary for simple tasks.
RECENT_MESSAGES_LIMIT = 4

# Warning threshold for LLM call cost in USD. If a call exceeds this, a warning will be printed in the console.
# For this project, my current goal is very roughly approx.
PRICE_WARNING = 0.0005

# Prevent infinite loops of tool calls.
CONSECUTIVE_TOOL_CALL_LIMIT = 5

SYSTEM_PROMPT = """
Answer in a very concise manner. Unless explicitly asked, respond with 1-2 very short sentences at most! 
NEVER use visual or structural formatting (e.g., markdown, headers, lists, symbols, emojis, line breaks).
You may still rewrite or normalize raw data (dates, times, numbers) into natural spoken language.
IMPORTANT: You can call tools to get information or perform actions. The output of the tool calls will be passed back to you in a different prompt afterwards. 
"""
