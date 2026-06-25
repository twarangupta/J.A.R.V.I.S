import pyaudio
import threading
from piper.voice import PiperVoice

class Speaker:
    """
    Modular text-to-speech speaker class using local neural Piper TTS.
    Provides the premium, original-sounding J.A.R.V.I.S. voice.
