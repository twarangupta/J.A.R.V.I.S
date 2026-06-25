import pyaudio
import numpy as np
import time
from config import SAMPLE_RATE, CHUNK_SIZE

class AudioHandler:
    """
    Manages microphone input streams.
    Provides methods to stream raw chunks for wake word detection,
    and to record complete phrases with basic silence detection for Whisper.
    """
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self):
        """Starts the microphone input stream."""
        if self.stream is not None:
            self.stop_stream()
            
        try:
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE
            )
        except Exception as e:
            print(f"[Audio Error] Failed to open microphone stream: {e}")
            raise e

    def stop_stream(self):
