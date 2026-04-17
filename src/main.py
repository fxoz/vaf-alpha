import os
import sys
import time

from rich import print

import mic
import agent
import sounds
import context

import kws.openww

from asr.mistral import MistralAsr as ASR
from tts.asynccom import AsyncComTts as TTS


chat = context.Chat()


def on_hotword():
    sounds.play_mp3("sounds/ok.mp3")

    recording_file = None
    try:
        recording_file = mic.record()
        prompt = ASR().transcribe(recording_file)
        print(f"[cyan]ASR:[/cyan] {prompt}")
    except Exception as e:
        print(f"[bold red]Mic/ASR Error:[/bold red] {e}")
    else:
        res = agent.handle_prompt(prompt=prompt, chat=chat)
        TTS().say(res)
    finally:
        if recording_file and os.path.exists(recording_file):
            os.remove(recording_file)


def main():
    print("[bold green]Ready![/bold green]")
    while True:
        kws.openww.loop()
        on_hotword()
        time.sleep(1.0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[bold red]Exiting...[/bold red]")
        sys.exit(0)
