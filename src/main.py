import os
import sys

import mic
import agent
import context

from asr.mistral import MistralAsr as ASR
from tts.asynccom import AsyncComTts as TTS

from rich import print

chat = context.Chat()

while True:
    recording_file = None
    try:
        recording_file = mic.record()
        prompt = ASR().transcribe(recording_file)
        print(f"[cyan]ASR:[/cyan] {prompt}")
    except Exception as e:
        print(f"[bold red]Mic/ASR Error:[/bold red] {e}")
        continue
    else:
        res = agent.handle_prompt(prompt=prompt, chat=chat)
        TTS().say(res)
    finally:
        if recording_file and os.path.exists(recording_file):
            os.remove(recording_file)
