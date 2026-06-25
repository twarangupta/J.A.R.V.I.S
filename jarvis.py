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
    """
    # Reset prediction buffers to clear the wake-up word trigger
    detector.reset()
    
    speak(text)
    
    # Start microphone stream to monitor for interrupt wake word
    audio_handler.start_stream()
    
    interrupted = False
    chunks_count = 0
    try:
        while is_speaking():
            # Keyboard interruption fallback
            if msvcrt.kbhit():
                msvcrt.getch() # Clear the keypress
                stop_speaking()
                interrupted = True
                print("\n[Speech interrupted by keyboard]")
                break
                
            chunk = audio_handler.read_chunk()
            chunks_count += 1
            
            # Check for wake word but ignore the first ~0.5 seconds (6 chunks)
            # of audio to prevent triggering from the trailing wake-up audio.
            if detector.is_wake_word(chunk):
                if chunks_count > 6:
                    stop_speaking()
                    interrupted = True
                    break
    finally:
        audio_handler.stop_stream()
        
    return interrupted

def main():
    print("=" * 50)
    print("                JARVIS INITIALIZATION                ")
    print("=" * 50)
    
    # 1. Initialize text-to-speech speaker
    speak("Initializing system protocols.")
    wait_speaking()

    # 2. Initialize Wake Word Detector
    try:
        detector = WakeWordDetector()
    except Exception as e:
        print(f"Failed to initialize Wake Word Detector: {e}")
        speak("Error loading wake word engine. Exiting.")
        wait_speaking()
        sys.exit(1)

    # 3. Initialize Faster-Whisper
    speak("Loading speech recognition models.")
    wait_speaking()
    print(f"Loading Faster-Whisper '{WHISPER_MODEL_SIZE}' model on '{WHISPER_DEVICE}' ({WHISPER_COMPUTE_TYPE})...")
    try:
        whisper_model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE
        )
        print("Speech recognition loaded successfully.")
    except Exception as e:
        print(f"Failed to initialize Whisper model: {e}")
        speak("Error loading speech recognition model. Exiting.")
        wait_speaking()
        sys.exit(1)

    speak("All systems active. Jarvis is online.")
    wait_speaking()

    # Main infinite loop
    while True:
        reset_brain() # Clear LLM context memory when entering sleep mode
        print("\n[Status: Sleeping] Standing by. Speak the wake word...")
        
        # Start continuous audio stream for wake word monitoring
        audio_handler.start_stream()
        
        while True:
            # Read streaming audio chunk
            chunk = audio_handler.read_chunk()
            
            # Check for wake word
            if detector.is_wake_word(chunk):
                break
                
        # Stop wake-word streaming to switch mode
        audio_handler.stop_stream()
        
        # Greeting (interruptible)
        interrupted = speak_and_interruptible("Systems online. How can I help you, sir?", detector)
        
        # Conversation loop
        while True:
            if interrupted:
                interrupted = False
                
            # Record user phrase with silence detection
            audio_data = audio_handler.record_phrase()
            
