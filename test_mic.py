import pyaudio
import numpy as np

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

pa = pyaudio.PyAudio()
print("Available input devices:")
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if info.get('maxInputChannels') > 0:
        print(f"Index {i}: {info.get('name')} (Channels: {info.get('maxInputChannels')})")

default_device = pa.get_default_input_device_info()
print(f"\nDefault input device: {default_device.get('name')} at index {default_device.get('index')}")

print("\nStarting stream. Speak into your mic (press Ctrl+C to stop)...")
