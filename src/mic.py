import math
import os
import shutil
import struct
import subprocess
import tempfile
import time
import wave

import sounddevice as sd

recordings_dir = "recordings"
if os.path.exists(recordings_dir):
    shutil.rmtree(recordings_dir)
os.makedirs(recordings_dir)


def record(
    sample_rate=16000,
    channels=1,
    silence_threshold=0.005,  # RMS threshold for "near-silence"
    silence_duration=1.2,  # seconds of near-silence before auto-stop
    min_record_seconds=0.4,  # avoid stopping immediately
    max_record_seconds=30.0,  # hard cap, safety only
    bitrate="10k",
    recordings_dir="recordings",
) -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found in PATH")

    os.makedirs(recordings_dir, exist_ok=True)
    out_path = os.path.join(recordings_dir, f"{int(time.time())}.opus")
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_wav.close()

    frames = []
    silence_started_at = None
    recording_started_at = None
    stop_requested = False

    def callback(indata, *_):
        nonlocal silence_started_at, recording_started_at, stop_requested

        now = time.time()
        recording_started_at = recording_started_at or now
        chunk = indata[:, 0]
        rms = math.sqrt(sum(float(x) * float(x) for x in chunk) / max(len(chunk), 1))
        frames.append(
            b"".join(
                struct.pack("<h", int(max(-1.0, min(1.0, float(x))) * 32767.0))
                for x in chunk
            )
        )

        elapsed = now - recording_started_at
        if elapsed >= max_record_seconds:
            stop_requested = True
            raise sd.CallbackStop()
        if rms < silence_threshold and elapsed >= min_record_seconds:
            silence_started_at = silence_started_at or now
            if now - silence_started_at >= silence_duration:
                stop_requested = True
                raise sd.CallbackStop()
        else:
            silence_started_at = None

    print("Recording... speak now.")

    cmd = [
        ffmpeg,
        "-y",
        "-i",
        tmp_wav.name,
        "-hide_banner",
        "-loglevel",
        "error",
        "-c:a",
        "libopus",
        "-b:a",
        bitrate,
        "-vbr",
        "on",
        "-application",
        "voip",
        out_path,
    ]

    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype="float32",
            callback=callback,
            blocksize=1024,
        ):
            while not stop_requested:
                sd.sleep(100)
    except sd.CallbackStop:
        pass
    finally:
        with wave.open(tmp_wav.name, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            for frame in frames:
                wf.writeframes(frame)

    try:
        subprocess.run(
            cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    finally:
        try:
            os.remove(tmp_wav.name)
        except OSError:
            pass

    return out_path


if __name__ == "__main__":
    record()
