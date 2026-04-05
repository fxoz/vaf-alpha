import os
import sys

import mic
import agent
import context

# ---
from asr.mistral import MistralAsr as ASR
from tts.asynccom import AsyncComTts as TTS
# ---

from rich import print

chat = context.Chat()

if len(sys.argv) < 2 or sys.argv[1] not in ("-t", "--text"):
    while True:
        recording_file = None
        try:
            recording_file = mic.record()
            prompt = ASR().transcribe(recording_file)
        except Exception as e:
            print(f"[bold red]Mic/ASR Error:[/bold red] {e}")
            continue
        else:
            res = agent.handle_prompt(prompt=prompt, chat=chat)
            TTS().say(res)
        finally:
            if recording_file and os.path.exists(recording_file):
                os.remove(recording_file)
else:
    while True:
        text_in = input(">>> ")
        res = agent.handle_prompt(prompt=text_in, chat=chat)
        TTS().say(res)
