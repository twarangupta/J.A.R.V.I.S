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

    def stop(self):
        """Instantly stops any ongoing playback."""
        self.stop_playback.set()
        if hasattr(self, 'out_stream') and self.out_stream:
            try:
                self.out_stream.stop_stream()
                self.out_stream.close()
            except:
                pass
            self.out_stream = None
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join()

    def wait(self):
        """Blocks until current speech is finished."""
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join()

    def speak(self, text: str):
        """
        Speaks the given text aloud asynchronously in a background thread.
        """
        self.stop()
        self.stop_playback.clear()
        print(f"\n[Jarvis]: {text}\n")
        
        if self.voice:
            try:
                # Generate audio bytes
