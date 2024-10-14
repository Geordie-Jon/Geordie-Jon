#!/usr/bin/env python3
# NOTE: this example requires PyAudio because it uses the Microphone class
import sys
import pathlib
import speech_recognition as sr
CHUNK = 1024


def get_audio() -> sr.AudioData | None:
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        return r.listen(source)


# Define the base path and name
base_path = pathlib.Path("./recordings")
base_name = "microphone-results"

# Define the different extensions
extensions = ("raw", "wav", "aiff", "flac")

# Create the recordings directory if it doesn't exist
base_path.mkdir(parents=True, exist_ok=True)

# Get the audio data
audio = get_audio()
if not audio:
    print("No audio detected")
    sys.exit(1)
# Save files with different extensions
for ext in extensions:
    file_path = base_path / f"{base_name}.{ext}"
    with open(file_path, "wb") as f:
        f.write(getattr(audio, f'get_{ext}_data')())
