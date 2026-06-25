import os
import numpy as np
from openwakeword.model import Model
from config import WAKE_WORD_MODEL, WAKE_WORD_THRESHOLD

class WakeWordDetector:
    """
    Wraps the OpenWakeWord library to monitor streaming audio chunks
    and detect the wake word.
    """
    def __init__(self):
        print(f"Initializing OpenWakeWord with model: {WAKE_WORD_MODEL}")
        
        # OpenWakeWord accepts file paths to custom models,
        # or names of built-in models (e.g. 'hey_jarvis')
        if os.path.exists(WAKE_WORD_MODEL):
            # If a custom path is specified, let openwakeword determine the framework or force onnx
            if WAKE_WORD_MODEL.endswith(".onnx"):
