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

