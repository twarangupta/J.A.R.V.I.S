import time
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

print("Loading voice model...")
voice = PiperVoice.load("models/jarvis-high.onnx")
print("Model loaded.")

text = "Hello Sir. I am Jarvis. Systems are fully functional."

print("Synthesizing...")
start = time.time()
audio_bytes = b""
for chunk in voice.synthesize(text):
    audio_bytes += chunk.audio_int16_bytes

print(f"Synthesized in {time.time() - start:.2f}s")

