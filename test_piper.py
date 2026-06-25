import time
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

print("Loading voice model...")
voice = PiperVoice.load("models/jarvis-high.onnx")
