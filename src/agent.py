import sys
import traceback

from rich import print

import config
import context
import config_skills

from llm._base import LlmResponse
from llm.openrouter import OpenRouterLlm as LLM
import skills._skill_usage

llm = LLM(skills._skill_usage.generate())


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
            assert call.name in config_skills.TOOL_REGISTRY, (
                f"Tool {call.name} not found in registry"
            )

            chat.add_tool_call(
                name=call.name, arguments=call.args, call_id=call.call_id
            )
            fn = config_skills.TOOL_REGISTRY[call.name]
            print(f"[magenta][bold]{call.name}[/bold]{call.args}[/magenta]")
            try:
                result = fn(**call.args)
            except Exception as e:
                result = f"Error calling tool: {e}"
                traceback.print_exc()
            chat.add_tool_call_output(call_id=call.call_id, output=result)

            print(f"->[green] {result}[/green]")


if __name__ == "__main__":
    if not sys.argv[1:]:
        print(
            "[red]Error: No prompt provided. Please provide a prompt as a command-line argument.[/red]"
        )
        sys.exit(1)

    chat = context.Chat()
    inp = " ".join([arg for arg in sys.argv[1:] if not arg.startswith("-")])
    handle_prompt(inp, chat)
