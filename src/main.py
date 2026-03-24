import os

from rich import print

import mic
import asr.mistral
import llm.cerebras
import tts.deepinfra

while True:
    try:
        recording_file = mic.record()
        text = asr.mistral.transcribe(recording_file)
        print(f"[bold green]You:[/bold green] {text}")
    except Exception as e:
        print(f"[bold red]Error:[/bold red] {e}")
        continue
    else:
        response = llm.cerebras.respond(text)
        print(f"[bold blue]VAF:[/bold blue] {response}")
        tts.deepinfra.say(response)
    finally:
        if os.path.exists(recording_file):
            os.remove(recording_file)
