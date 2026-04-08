import os
import datetime
import pvporcupine

from rich import print
from pvrecorder import PvRecorder

ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
KEYWORD = "jarvis"


def on_wake_word_detected():
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 🟢 Wake word '{KEYWORD}' detected! Ready for your command...")


def list_audio_devices():
    devices = PvRecorder.get_available_devices()
    print("Available audio input devices:")
    for i, device in enumerate(devices):
        print(f"  [{i}] {device}")
    print()


def main():
    porcupine = None
    recorder = None

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY, keywords=[KEYWORD], sensitivities=[0.5]
        )

        recorder = PvRecorder(
            device_index=-1,
            frame_length=porcupine.frame_length,
        )

        print(f"\n[green]Listening for '{KEYWORD}'... (Press Ctrl+C to stop)[/green]\n")
        recorder.start()

        while True:
            audio_frame = recorder.read()
            keyword_index = porcupine.process(audio_frame)

            if keyword_index >= 0:
                on_wake_word_detected()

    except pvporcupine.PorcupineInvalidArgumentError:
        print("[red][ERROR] Invalid Porcupine access key.[/red]")
    except pvporcupine.PorcupineActivationError:
        print(
            "[red][ERROR] Access key activation failed. Check your key and internet connection.[/red]"
        )
    except KeyboardInterrupt:
        print("\n\nStopped")
    finally:
        if recorder is not None:
            recorder.stop()
            recorder.delete()
        if porcupine is not None:
            porcupine.delete()


if __name__ == "__main__":
    main()
