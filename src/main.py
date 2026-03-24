import os
import shutil

import asr
import mic
import llm
import tts

from rich import print

while True:
    try:
        recording_file = mic.record()

        text = asr.transcribe(recording_file)
        print(f"[bold green]You:[/bold green] {text}")
    except Exception as e:
        print(f"[bold red]Error:[/bold red] {e}")
        continue
    else:
        response = llm.respond(text)

        print(f"[bold blue]VAF:[/bold blue] {response}")
        tts.say(response)
    finally:
        if os.path.exists(recording_file):
            os.remove(recording_file)
