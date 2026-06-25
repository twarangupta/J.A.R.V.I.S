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
                self.model = Model(wakeword_models=[WAKE_WORD_MODEL], inference_framework="onnx")
            else:
                self.model = Model(wakeword_models=[WAKE_WORD_MODEL])
        else:
            self.model = Model(wakeword_models=[WAKE_WORD_MODEL], inference_framework="onnx")
            
        # Get the internal key used to access prediction buffers
        self.model_key = list(self.model.models.keys())[0]
        print(f"Wake word model loaded. Key name: {self.model_key}")

    def is_wake_word(self, chunk: np.ndarray) -> bool:
