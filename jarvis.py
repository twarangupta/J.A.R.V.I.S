from config import (
    WHISPER_MODEL_SIZE,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE,
    WHISPER_LANGUAGE,
    WHISPER_VAD_FILTER,
    SLEEP_WORD
)
import sys
import msvcrt
import numpy as np
from faster_whisper import WhisperModel
from audio import audio_handler
from wakeword import WakeWordDetector
from brain import ask_ai, reset_brain
from commands import execute_command
from speaker import speak, stop_speaking, wait_speaking, is_speaking

def speak_and_interruptible(text: str, detector: WakeWordDetector) -> bool:
    """
    Plays the response. While speaking, continuously streams mic audio and checks for the wake word.
    If the wake word is detected, stops speaking immediately and returns True.
