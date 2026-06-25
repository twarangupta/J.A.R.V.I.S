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

# Convert bytes to numpy array
audio_data = np.frombuffer(audio_bytes, dtype=np.int16)

# Play audio
sample_rate = voice.config.sample_rate
print(f"Playing at sample rate: {sample_rate}Hz...")
sd.play(audio_data, sample_rate)
