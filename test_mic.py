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
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE
)

try:
    while True:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        chunk = np.frombuffer(data, dtype=np.int16)
        max_amplitude = np.max(np.abs(chunk))
        mean_amplitude = np.mean(np.abs(chunk))
        print(f"Max Amplitude: {max_amplitude:5d} | Mean Amplitude: {mean_amplitude:5.1f} | " + ("#" * int(min(max_amplitude, 5000) / 100)), end="\r")
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    stream.stop_stream()
    stream.close()
