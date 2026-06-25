from config import (
    WHISPER_MODEL_SIZE,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE,
    WHISPER_LANGUAGE,
    WHISPER_VAD_FILTER,
    SLEEP_WORD
)
import sys
import numpy as np
from faster_whisper import WhisperModel
from audio import audio_handler, check_keyboard_hit, clear_keyboard_hit
from wakeword import WakeWordDetector
from brain import ask_ai, reset_brain
from commands import execute_command
from speaker import speak, stop_speaking, wait_speaking, is_speaking
from logger import logger

def get_startup_greeting() -> str:
    import random
    import urllib.request
    import json
    import psutil

    candidates = []

    # 1. Attempt Weather/Location Lookup (max 1.5s timeout)
    weather_text = None
    try:
        req = urllib.request.Request(
            "http://ip-api.com/json/",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=1.5) as response:
            data = json.loads(response.read().decode())
            city = data.get("city")
            lat = data.get("lat")
            lon = data.get("lon")
            
        if city and lat is not None and lon is not None:
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            req2 = urllib.request.Request(
                weather_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req2, timeout=1.5) as response:
                weather_data = json.loads(response.read().decode())
                temp = weather_data.get("current_weather", {}).get("temperature")
                if temp is not None:
                    weather_templates = [
                        f"According to your IP address, it is currently {temp} degrees Celsius in {city}, sir.",
                        f"The weather in {city} is {temp} degrees Celsius right now, sir. Hopefully, it's a good day to build.",
                        f"I've checked the local conditions in {city}. It's currently {temp} degrees Celsius, sir."
                    ]
                    weather_text = random.choice(weather_templates)
    except Exception:
        pass

    if weather_text:
        candidates.append(weather_text)

    # 2. Attempt Battery Check
    battery_text = None
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            percent = battery.percent
            status = "connected to AC power" if battery.power_plugged else "running on battery power"
            battery_templates = [
                f"All protocols initialized, sir. Battery is at {percent} percent, and we are currently {status}.",
                f"Jarvis is online, sir. Power levels are at {percent} percent and we are {status}.",
                f"System check complete, sir. Internal power is at {percent} percent, and we are {status}."
            ]
            battery_text = random.choice(battery_templates)
    except Exception:
        pass

    if battery_text:
        candidates.append(battery_text)

    # 3. Conversational/Iron Man style greetings & questions (always present)
    conversational_options = [
        "Welcome back, sir. Repulsor power at 100 percent. Shall we run a diagnostics check?",
        "All systems are green, sir. Ready for your instructions.",
        "Jarvis is online, sir. Do you have any plans for upgrading the suit design today?",
        "System initialization complete. What are we coding today, sir?",
        "Tony would be proud of this setup. What is our next objective, sir?",
        "Greetings, sir. I've cleared the caches. Shall we proceed?",
        "Online and ready, sir. Would you like me to scan for any security alerts?",
        "Diagnostics complete, sir. Repulsors, flight stabilizer, and cooling systems are all optimal. What's next?",
        "Welcome back, sir. I hope you're ready to make some magic today. Where should we start?",
        "All auxiliary systems are operating within normal parameters. What can I do for you today, sir?"
    ]
    candidates.append(random.choice(conversational_options))

    # Pick exactly one greeting
    return random.choice(candidates)

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
            if check_keyboard_hit():
                clear_keyboard_hit()
                stop_speaking()
                interrupted = True
                logger.info("Speech interrupted by keyboard")
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
    
    # Play premium repulsor startup tone
    try:
        from startup_audio import play_startup_sound
        play_startup_sound()
    except:
        pass
    
    # 1. Initialize text-to-speech speaker
    speak("Initializing system protocols.")
    wait_speaking()

    # 2. Initialize Wake Word Detector
    try:
        detector = WakeWordDetector()
    except Exception as e:
        logger.error(f"Failed to initialize Wake Word Detector: {e}")
        speak("Error loading wake word engine. Exiting.")
        wait_speaking()
        sys.exit(1)

    # 3. Initialize Faster-Whisper
    speak("Loading speech recognition models.")
    wait_speaking()
    logger.info(f"Loading Faster-Whisper '{WHISPER_MODEL_SIZE}' model on '{WHISPER_DEVICE}' ({WHISPER_COMPUTE_TYPE})...")
    try:
        whisper_model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE
        )
        logger.info("Speech recognition loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Whisper model: {e}")
        speak("Error loading speech recognition model. Exiting.")
        wait_speaking()
        sys.exit(1)

    greeting_text = get_startup_greeting()
    logger.info(f"Jarvis Startup Greeting: {greeting_text}")
    speak(greeting_text)
    wait_speaking()

    # Main infinite loop
    while True:
        reset_brain() # Clear LLM context memory when entering sleep mode
        logger.info("Status: Sleeping. Standing by. Speak the wake word...")
        
        # Start continuous audio stream for wake word monitoring
        import time
        if not audio_handler.start_stream():
            logger.error("Microphone hardware connection is missing or blocked. Retrying in 5 seconds...")
            time.sleep(5)
            continue
        
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
            
            # Skip if no audio recorded
            if len(audio_data) == 0:
                continue
                
            logger.info("Transcribing...")
            try:
                segments, info = whisper_model.transcribe(
                    audio_data,
                    beam_size=5,
                    language=WHISPER_LANGUAGE,
                    vad_filter=WHISPER_VAD_FILTER
                )
                transcription = "".join(seg.text for seg in segments).strip()
            except Exception as e:
                logger.error(f"Transcription error: {e}")
                transcription = ""
                
            if not transcription:
                logger.info("No speech recognized")
                continue
                
            print(f"You: {transcription}")
            
            # Check for sleep trigger
            if SLEEP_WORD in transcription.lower():
                speak("Understood. Re-engaging sleep mode.")
                wait_speaking()
                try:
                    from startup_audio import play_sleep_sound
                    play_sleep_sound()
                except:
                    pass
                break
                
            # Check if this is a direct system command
            command_response = execute_command(transcription)
            
            if command_response is not None:
                if command_response == "":
                    interrupted = False
                else:
                    interrupted = speak_and_interruptible(command_response, detector)
            else:
                # Query Ollama Brain
                ai_response = ask_ai(transcription)
                
                # Check for AI-routed command tag
                import re
                match = re.search(r"COMMAND:\s*([a-zA-Z0-9_\-\s]+)", ai_response, re.IGNORECASE)
                if match:
                    extracted_cmd = match.group(1).strip()
                    # Clean the speech reply by removing the command block
                    natural_reply = re.sub(r"[`\[]*[^`\[]*COMMAND:\s*[^\]`]+[\]`]*", "", ai_response, flags=re.IGNORECASE).strip()
                    
                    logger.info(f"AI Command Routed: Executing extracted command: '{extracted_cmd}'")
                    cmd_res = execute_command(extracted_cmd)
                    
                    # If the command returned an error or failure, speak the failure message
                    if cmd_res and ("failed" in cmd_res.lower() or "error" in cmd_res.lower() or "unable" in cmd_res.lower()):
                        interrupted = speak_and_interruptible(cmd_res, detector)
                    elif cmd_res == "":
                        interrupted = False
                    else:
                        speech_text = natural_reply if natural_reply else (cmd_res if cmd_res else "Command executed, sir.")
                        interrupted = speak_and_interruptible(speech_text, detector)
                else:
                    interrupted = speak_and_interruptible(ai_response, detector)
                
            if interrupted:
                logger.info("Speech interrupted by user")
                continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Jarvis going offline.")
        stop_speaking()
        speak("Goodbye, sir. Going offline.")
        wait_speaking()
        audio_handler.terminate()
        sys.exit(0)