import os
import sys
import time
import shutil
import traceback

from rich import print
from yaspin import yaspin
from rich.console import Console

import config
import context
import skills._skill_usage


from llm._base import LlmResponse
from llm.openrouter import OpenRouterLlm as LLM
from skills.web import init_browser

llm = LLM(skills._skill_usage.TOOL_DEFINITIONS)

if os.path.exists("logs"):
    shutil.rmtree("logs")
os.makedirs("logs", exist_ok=True)

if "-p" not in sys.argv:
    init_browser()


def handle_tool_call(call: context.ToolCall, chat: context.Chat) -> None:
    if call.name not in skills._skill_usage.TOOL_REGISTRY:
        raise ValueError(f"Tool {call.name} not found in registry")

    chat.add_tool_call(name=call.name, arguments=call.args, call_id=call.call_id)
    fn = skills._skill_usage.TOOL_REGISTRY[call.name]
    print(f"[magenta][bold]{call.name}[/bold]{call.args}[/magenta]")

    start = time.time()
    try:
        with yaspin(text="⌛ Using skill...", color="cyan") as _:
            result = fn(**call.args)
    except Exception as e:
        result = f"Error calling tool: {e}"
        traceback.print_exc()

        if not config.ALLOW_TOOL_ERRORS:
            raise

    if time.time() - start > 1.0:
        print(f"[yellow]Tool call took {time.time() - start:.2f} seconds[/yellow]")

    chat.add_tool_call_output(call_id=call.call_id, output=result)

    result_short = str(result).replace("\n", "↵ ")
    if len(result_short) > 100:
        result_short = result_short[:100] + "..."

    print(f"->[green] {result_short}[/green]")


def handle_prompt(prompt: str, chat: context.Chat) -> str:
    final_text = "Done."
    chat.add_user_message(prompt)

    # +1 because a "normal", non-tool-calling response from the LLM is ALSO handled inside of this loop.
    for _ in range(config.CONSECUTIVE_TOOL_CALL_LIMIT + 1):
        res: LlmResponse = llm.respond(chat)

        if res.text:
            chat.add_ai_message(res.text)
            print(f"[blue]LLM: [bold]{res.text}[/bold][/blue]")
            final_text = res.text

        if not res.tool_calls:
            return final_text  # we're entirely done with this user prompt.

        for call in res.tool_calls:
            handle_tool_call(call, chat)


if __name__ == "__main__":
    chat = context.Chat()
    console = Console()

    if not [arg for arg in sys.argv[1:] if not arg.startswith("-")]:
        while True:
            inp = console.input("[bold magenta]Enter your prompt: [/bold magenta]")
            handle_prompt(inp, chat)

    inp = " ".join([arg for arg in sys.argv[1:] if not arg.startswith("-")])
    handle_prompt(inp, chat)
