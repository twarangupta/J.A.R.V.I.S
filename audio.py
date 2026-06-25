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
