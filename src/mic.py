import os
import time
import math
import wave
import shutil
import struct
import tempfile
import subprocess

import sounddevice as sd


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

    timestamp = int(time.time())
    out_path = os.path.join(recordings_dir, f"{timestamp}.opus")

    # Temporary WAV file for ffmpeg input
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_wav.close()

    frames = []
    silence_started_at = None
    recording_started_at = None
    stop_requested = False

    def callback(indata, frames_count, time_info, status):
        nonlocal silence_started_at, recording_started_at, stop_requested

        if status:
            print(f"audio status: {status}")

        now = time.time()
        if recording_started_at is None:
            recording_started_at = now

        # indata is float32 in range about [-1.0, 1.0]
        chunk = indata[:, 0]

        # Compute RMS
        sq = 0.0
        for x in chunk:
            sq += float(x) * float(x)
        rms = math.sqrt(sq / max(len(chunk), 1))

        # Store as 16-bit PCM for WAV writing
        pcm16 = bytearray()
        for x in chunk:
            s = max(-1.0, min(1.0, float(x)))
            pcm16 += struct.pack("<h", int(s * 32767.0))
        frames.append(bytes(pcm16))

        elapsed = now - recording_started_at

        # Silence detection
        if rms < silence_threshold and elapsed >= min_record_seconds:
            if silence_started_at is None:
                silence_started_at = now
            elif (now - silence_started_at) >= silence_duration:
                stop_requested = True
                raise sd.CallbackStop()
        else:
            silence_started_at = None

        # Hard max duration
        if elapsed >= max_record_seconds:
            stop_requested = True
            raise sd.CallbackStop()

    print("Recording... speak now.")

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
    finally:
        # Write WAV
        with wave.open(tmp_wav.name, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # int16
            wf.setframerate(sample_rate)
            for frame in frames:
                wf.writeframes(frame)

    # Convert WAV -> Opus with ffmpeg
    # -application voip is appropriate for a simple voice assistant
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        tmp_wav.name,
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
        subprocess.run(cmd, check=True)
    finally:
        try:
            os.remove(tmp_wav.name)
        except OSError:
            pass

    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    record()
