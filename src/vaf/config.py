CALENDAR_CACHE_SECONDS: int = 600

CALENDAR_CONTEXT_MAX_ITEMS: int = 20
CALENDAR_CONTEXT_MAX_DAYS: int = 7

# as opposed to a hosted server version without access to i.e. desktop OCR
LOCAL_MODE: bool = True

BROWSE_HEADLESS: bool = True

# no = raise exceptions and crash the program
ALLOW_TOOL_ERRORS: bool = False

# drastically reduces first web skill call latency, but increases startup time and resource usage!
# ? Tip! Disable using -p in agent.py
PREPARE_BROWSER_ON_STARTUP: bool = True

# MODEL_LLM_BASIC = "openai/gpt-oss-safeguard-20b"
# MODEL_LLM_BASIC = "mistralai/codestral-2508"
# MODEL_LLM_BASIC: str = "qwen/qwen3.5-flash-02-23"
MODEL_LLM_BASIC: str = "openai/gpt-oss-120b"
MODEL_LLM_BASIC_TEMPERATURE: float = 0.2
MODEL_LLM_BASIC_MAX_TOKENS: int = 4096
MODEL_LLM_BASIC_REASONING: str = "minimal"
MODEL_LLM_BASIC_OPENROUTER_ENFORCE_PROVIDER: str | None = None  # "google-vertex"

MODEL_OCR: str = "google/gemini-3.1-flash-lite-preview"

TIMEOUT_LLM_BASIC: float = 10.0
TIMEOUT_OCR: float = 10.0
TIMEOUT_WEB: float = 10.0
TIMEOUT_WEB_TREE: float = 15.0

BANNED_DOMAINS: list[str] = [
    "google.com",
    "youtube.com",
    "facebook.com",
    "linkedin.com",
    "trends.google.com",
]

SYSTEM_PROMPT: str = """
Answer in a very concise manner. Unless explicitly asked, respond with 1-2 very short sentences at most! 
NEVER use visual or structural formatting (e.g., markdown, headers, lists, symbols, emojis, line breaks).
You may still rewrite or normalize raw data (dates, times, numbers) into natural spoken language.
IMPORTANT: You can call tools to get information or perform actions. The output of the tool calls will be passed back to you in a different prompt afterwards.
If a tool doesn't return anything, it means it executed successfully but returned no output.
Only use MemorySkill if "notes", "remember", "recall", "save", "write down" or any similar terms are mentioned, but not without no specific reason.
Use the web search skill (if available) for up-to-date info, research, finance, weather, sports and similar.
ALWAYS respond in the language used in the prompt, unless explicitly asked to switch to a different language or to translate. 
"""

# For every LLM call, we include the initial system prompt + the most recent N messages in the conversation history.
# Low values save tokens -> money, but may reduce response quality/accuracy. Very high values (e.g., 10 or more) may be unnecessary for simple tasks.
RECENT_MESSAGES_LIMIT: int = 4

# Warning threshold for LLM call cost in USD. If a call exceeds this, a warning will be printed in the console.
# For this project, my current goal is very roughly approx.
PRICE_WARNING: float = 0.0005

# Prevent infinite loops of tool calls.
CONSECUTIVE_TOOL_CALL_LIMIT: int = 5
