import os
import sys

import mic
import context

# ---
from asr.mistral import MistralAsr as ASR
from tts.asynccom import AsyncComTts as TTS
from llm.openrouter import OpenRouterLlm as LLM
# ---

from rich import print

if len(sys.argv) < 2 or sys.argv[1] not in ("-t", "--text"):
    while True:
        recording_file = None
        try:
            recording_file = mic.record()
            text_in = ASR().transcribe(recording_file)
            context.add_user(text_in)
            print(f"[bold green]You:[/bold green] {text_in}")
        except Exception as e:
            print(f"[bold red]Error:[/bold red] {e}")
            continue
        else:
            text_out = LLM().respond(context.get())
            context.add_ai(text_out)
            print(f"[bold blue]VAF:[/bold blue] {text_out}")
            TTS().say(text_out)
        finally:
            if recording_file and os.path.exists(recording_file):
                os.remove(recording_file)
else:
    while True:
        text_in = input(">>> ")
        context.add_user(text_in)
        text_out = LLM().respond(context.get())
        context.add_ai(text_out)
        print(f"[bold blue]VAF:[/bold blue] {text_out}")
