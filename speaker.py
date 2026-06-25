import pyaudio
import threading
from piper.voice import PiperVoice

class Speaker:
    """
    Modular text-to-speech speaker class using local neural Piper TTS.
    Provides the premium, original-sounding J.A.R.V.I.S. voice.
    Supports non-blocking background playback and instant interruption.
    """
    def __init__(self):
        try:
            print("[TTS Initialization] Loading J.A.R.V.I.S. neural voice model...")
            self.voice = PiperVoice.load("models/jarvis-high.onnx")
            self.sample_rate = self.voice.config.sample_rate
            self.pa = pyaudio.PyAudio()
            self.play_thread = None
            self.stop_playback = threading.Event()
            self.is_speaking = False
            print("[TTS Initialization] J.A.R.V.I.S. neural voice loaded successfully.")
        except Exception as e:
            print(f"Error loading J.A.R.V.I.S. voice model: {e}")
            self.voice = None

