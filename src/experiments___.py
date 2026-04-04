# from skills.memory import MemorySkill

# MemorySkill().write("abc123", "This is a new test memory.")
# print(MemorySkill().list_all())
# print(MemorySkill().read("abc123"))

import skills._skill_usage

from rich import print
from llm.openrouter import OpenRouterLlm as LLM

res: str = LLM(skills._skill_usage.generate()).respond(
    [{"role": "user", "content": "what's the current time?"}]
)
print(res)
