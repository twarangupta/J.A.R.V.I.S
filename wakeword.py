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
        
