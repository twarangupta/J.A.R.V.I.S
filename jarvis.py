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
